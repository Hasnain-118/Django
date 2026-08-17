from decimal import Decimal
import requests

from django.core.files.base import ContentFile
from django.db import models


# =========================================================
# CONTACT MODEL
# =========================================================

class Contact(models.Model):

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=35)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
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

    author = models.CharField(
        max_length=100,
        blank=True
    )

    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )

    quote = models.TextField(
        blank=True
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=Decimal('0.0')
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='fiction'
    )

    pdf_file = models.FileField(
        upload_to='book_pdfs/',
        blank=True,
        null=True
    )

    external_link = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


    # =====================================================
    # FETCH COVER FROM OPEN LIBRARY
    # =====================================================

    def fetch_cover_from_open_library(self):

        query = self.title.strip()

        if self.author:
            query += f" {self.author.strip()}"

        print(f"\nSearching Open Library for: {query}")

        try:

            response = requests.get(
                "https://openlibrary.org/search.json",
                params={
                    "q": query,
                    "limit": 10,
                },
                headers={
                    "User-Agent": "HasnainsDigitalLibrary/1.0"
                },
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            books = data.get("docs", [])

            print(
                f"Open Library results: {len(books)}"
            )

            if not books:
                print(
                    f"No result found for: {self.title}"
                )
                return


            # =================================================
            # FIRST: TRY COVER ID
            # =================================================

            for result in books:

                cover_id = result.get("cover_i")

                if not cover_id:
                    continue

                image_url = (
                    "https://covers.openlibrary.org/"
                    f"b/id/{cover_id}-L.jpg"
                )

                print(
                    f"Trying cover ID: {cover_id}"
                )

                image_response = requests.get(
                    image_url,
                    headers={
                        "User-Agent":
                            "HasnainsDigitalLibrary/1.0"
                    },
                    timeout=10
                )

                if image_response.status_code != 200:
                    continue

                content_type = image_response.headers.get(
                    "Content-Type",
                    ""
                )

                if not content_type.startswith("image/"):
                    continue

                # Avoid Open Library placeholder image
                if len(image_response.content) < 5000:
                    continue

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
                    ContentFile(
                        image_response.content
                    ),
                    save=False
                )

                print(
                    f"SUCCESS: Cover downloaded for "
                    f"{self.title}"
                )

                return


            # =================================================
            # SECOND: TRY ISBN
            # =================================================

            print(
                "No usable cover ID found. "
                "Trying ISBN..."
            )

            for result in books:

                isbn_list = result.get(
                    "isbn",
                    []
                )

                if not isbn_list:
                    continue

                for isbn in isbn_list[:5]:

                    image_url = (
                        "https://covers.openlibrary.org/"
                        f"b/isbn/{isbn}-L.jpg"
                    )

                    image_response = requests.get(
                        image_url,
                        headers={
                            "User-Agent":
                                "HasnainsDigitalLibrary/1.0"
                        },
                        timeout=10
                    )

                    if image_response.status_code != 200:
                        continue

                    content_type = (
                        image_response.headers.get(
                            "Content-Type",
                            ""
                        )
                    )

                    if not content_type.startswith(
                        "image/"
                    ):
                        continue

                    # Avoid placeholder images
                    if len(image_response.content) < 5000:
                        continue

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
                        ContentFile(
                            image_response.content
                        ),
                        save=False
                    )

                    print(
                        f"SUCCESS: Cover downloaded "
                        f"using ISBN for {self.title}"
                    )

                    return


            # =================================================
            # NO COVER FOUND
            # =================================================

            print(
                f"NO COVER AVAILABLE: "
                f"{self.title}"
            )

        except requests.RequestException as e:

            print(
                f"Open Library request error "
                f"for {self.title}: {e}"
            )

        except Exception as e:

            print(
                f"Unexpected error fetching cover "
                f"for {self.title}: {e}"
            )


    # =====================================================
    # AUTOMATIC COVER FETCH
    # =====================================================

    def save(self, *args, **kwargs):

        # If the user did not upload a cover,
        # automatically try Open Library.

        if not self.cover_image:

            self.fetch_cover_from_open_library()

        super().save(*args, **kwargs)