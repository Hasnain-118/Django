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


# =========================================================
# BOOK MODEL
# =========================================================

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

    # OPTIONAL
    # If user does not upload a cover,
    # Open Library will try to find one.
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

        query = self.title

        if self.author:
            query += f" {self.author}"

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

            if not books:
                print(
                    f"No Open Library result found for: {self.title}"
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
                    f"https://covers.openlibrary.org/"
                    f"b/id/{cover_id}-L.jpg"
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

                # Make sure response is actually an image
                content_type = image_response.headers.get(
                    "Content-Type",
                    ""
                )

                if not content_type.startswith("image/"):
                    continue

                file_name = (
                    self.title
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                    + ".jpg"
                )

                self.cover_image.save(
                    file_name,
                    ContentFile(image_response.content),
                    save=False
                )

                print(
                    f"Cover downloaded for: {self.title}"
                )

                return


            # =================================================
            # SECOND: TRY ISBN
            # =================================================

            for result in books:

                isbn_list = result.get("isbn", [])

                if not isbn_list:
                    continue

                # Try first few ISBNs instead of only one
                for isbn in isbn_list[:5]:

                    image_url = (
                        f"https://covers.openlibrary.org/"
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

                    content_type = image_response.headers.get(
                        "Content-Type",
                        ""
                    )

                    if not content_type.startswith("image/"):
                        continue

                    file_name = (
                        self.title
                        .replace(" ", "_")
                        .replace("/", "_")
                        .replace("\\", "_")
                        + ".jpg"
                    )

                    self.cover_image.save(
                        file_name,
                        ContentFile(image_response.content),
                        save=False
                    )

                    print(
                        f"Cover downloaded using ISBN: "
                        f"{self.title}"
                    )

                    return


            print(
                f"No cover available for: {self.title}"
            )

        except requests.RequestException as e:

            print(
                f"Open Library error for "
                f"{self.title}: {e}"
            )


    # =====================================================
    # AUTOMATIC COVER FETCH
    # =====================================================

    def save(self, *args, **kwargs):

        # Only fetch automatically when
        # user did NOT upload a cover.

        if not self.cover_image:

            self.fetch_cover_from_open_library()

        super().save(*args, **kwargs)