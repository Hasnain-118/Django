from decimal import Decimal
import requests

from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=35)
    phone = models.CharField(max_length=12)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('manga', 'Manga'),
        ('manhwa', 'Manhwa'),
        ('classic', 'Classics'),
        ('mystery', 'Mystery & Thriller'),
        ('romance', 'Romance'),
        ('fantasy', 'Fantasy'),
        ('sci-fi', 'Science Fiction'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    quote = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='fiction')
    pdf_file = models.FileField(upload_to='book_pdfs/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True, default=0)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        try:
            if self.cover_image:
                return self.cover_image.url
        except Exception:
            return ''
        return ''

    def fetch_book_data_from_open_library(self):
        """Fetch book data from Open Library - Working version"""
        
        title_query = self.title.strip()
        if self.author:
            title_query += f" {self.author.strip()}"

        print(f"\n{'='*50}")
        print(f"FETCHING FROM OPEN LIBRARY: {title_query}")
        print(f"{'='*50}")
        
        try:
            # Search Open Library
            response = requests.get(
                "https://openlibrary.org/search.json",
                params={"q": title_query, "limit": 10},
                headers={"User-Agent": "HasnainsDigitalLibrary/1.0"},
                timeout=15
            )

            response.raise_for_status()
            data = response.json()
            books = data.get("docs", [])

            print(f"Open Library results: {len(books)}")

            if not books:
                print(f"No results found")
                return

            # Find best match
            best_match = None
            for result in books:
                result_title = result.get('title', '').lower()
                if self.title.lower() == result_title:
                    if 'sparknotes' not in result_title and 'study guide' not in result_title:
                        best_match = result
                        break
            
            if not best_match:
                for result in books:
                    result_title = result.get('title', '').lower()
                    if self.title.lower() in result_title:
                        if 'sparknotes' not in result_title and 'study guide' not in result_title:
                            best_match = result
                            break
            
            if not best_match:
                best_match = books[0]

            print(f"Best match: {best_match.get('title')}")

            # Get OLID
            olid = None
            if best_match.get('key'):
                olid = best_match['key'].replace('/works/', '')
                print(f"OLID: {olid}")

            # =============================================
            # FETCH DESCRIPTION FROM DETAILS API
            # =============================================
            if olid:
                detail_url = f"https://openlibrary.org/works/{olid}.json"
                print(f"Fetching description from details API...")

                try:
                    detail_response = requests.get(
                        detail_url,
                        headers={"User-Agent": "HasnainsDigitalLibrary/1.0"},
                        timeout=15
                    )

                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()

                        if detail_data.get('description'):
                            if isinstance(detail_data['description'], dict):
                                description = detail_data['description'].get('value', '')
                            else:
                                description = detail_data['description']
                            
                            if description:
                                self.description = description
                                print(f"Description: {description[:100]}...")
                            else:
                                print(f"Description field is empty")
                        else:
                            print(f"No description field in details response")

                except Exception as e:
                    print(f"Error fetching description: {e}")
            else:
                print(f"No OLID found, cannot fetch description")

            # =============================================
            # PUBLISHER
            # =============================================
            publishers = best_match.get('publisher', [])
            if publishers:
                self.publisher = ', '.join(publishers[:3])
                print(f"Publisher: {self.publisher}")
            else:
                print(f"Publisher: Not available")

            # =============================================
            # PUBLISHED DATE
            # =============================================
            publish_dates = best_match.get('publish_date', [])
            if publish_dates:
                self.published_date = publish_dates[0]
                print(f"Published: {self.published_date}")
            else:
                print(f"Published: Not available")

            # =============================================
            # PAGE COUNT
            # =============================================
            if best_match.get('number_of_pages'):
                self.page_count = best_match['number_of_pages']
                print(f"Pages: {self.page_count}")
            else:
                print(f"Pages: Not available")

            # =============================================
            # ISBN
            # =============================================
            isbn_list = best_match.get('isbn', [])
            if isbn_list:
                self.isbn = isbn_list[0]
                print(f"ISBN: {self.isbn}")
            else:
                print(f"ISBN: Not available")

            # =============================================
            # COVER IMAGE
            # =============================================
            cover_id = best_match.get("cover_i")
            if cover_id and not self.cover_image:
                for size in ['-L.jpg', '-M.jpg']:
                    image_url = f"https://covers.openlibrary.org/b/id/{cover_id}{size}"
                    print(f"Trying cover: {image_url}")

                    try:
                        image_response = requests.get(
                            image_url,
                            headers={"User-Agent": "HasnainsDigitalLibrary/1.0"},
                            timeout=10
                        )

                        if image_response.status_code == 200:
                            content_type = image_response.headers.get("Content-Type", "")
                            if content_type.startswith("image/") and len(image_response.content) >= 5000:
                                file_name = (
                                    self.title
                                    .strip()
                                    .replace(" ", "_")
                                    .replace("/", "_")
                                    .replace("\\", "_")
                                    .replace(":", "_")
                                    + ".jpg"
                                )

                                self.cover_image.save(
                                    file_name,
                                    ContentFile(image_response.content),
                                    save=False
                                )
                                print(f"Cover downloaded!")
                                break
                    except Exception as e:
                        print(f"Error: {e}")
                        continue

            if isbn_list and not self.cover_image:
                print("Trying ISBN for cover...")
                for isbn in isbn_list[:3]:
                    for size in ['-L.jpg', '-M.jpg']:
                        try:
                            image_url = f"https://covers.openlibrary.org/b/isbn/{isbn}{size}"
                            image_response = requests.get(
                                image_url,
                                headers={"User-Agent": "HasnainsDigitalLibrary/1.0"},
                                timeout=10
                            )

                            if image_response.status_code == 200:
                                content_type = image_response.headers.get("Content-Type", "")
                                if content_type.startswith("image/") and len(image_response.content) >= 5000:
                                    file_name = (
                                        self.title
                                        .strip()
                                        .replace(" ", "_")
                                        .replace("/", "_")
                                        .replace("\\", "_")
                                        .replace(":", "_")
                                        + ".jpg"
                                    )

                                    self.cover_image.save(
                                        file_name,
                                        ContentFile(image_response.content),
                                        save=False
                                    )
                                    print(f"Cover downloaded using ISBN!")
                                    break
                        except Exception as e:
                            print(f"Error: {e}")
                            continue
                    if self.cover_image:
                        break

            if not self.cover_image:
                print(f"No cover available")

        except requests.RequestException as e:
            print(f"Open Library request error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        print(f"\n{'='*50}")
        print(f"FETCH COMPLETE")
        print(f"{'='*50}")

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.cover_image or not self.description:
            self.fetch_book_data_from_open_library()

        super().save(*args, **kwargs)

        if is_new:
            for user in User.objects.all():
                Notification.objects.create(
                    user=user,
                    message=f"New book added: {self.title}",
                    link=f"/read/{self.pk}/"
                )


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.CharField(max_length=200)
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message}"