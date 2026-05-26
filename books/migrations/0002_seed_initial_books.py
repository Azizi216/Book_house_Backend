from django.db import migrations


def seed_books(apps, schema_editor):
    Book = apps.get_model('books', 'Book')

    if Book.objects.exists():
        return

    Book.objects.bulk_create([
        Book(
            title='Atomic Habits',
            author='James Clear',
            category='Self Help',
            image_url='/book_house.png',
            rating=4.8,
            year=2018,
            pages=320,
            description='A practical book about building good habits with small daily actions.',
        ),
        Book(
            title='Clean Code',
            author='Robert C. Martin',
            category='Technology',
            image_url='/land2.jpg',
            rating=4.7,
            year=2008,
            pages=464,
            description='A software engineering book about writing readable and maintainable code.',
        ),
        Book(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            category='Novel',
            image_url='/land3.jpg',
            rating=4.4,
            year=1925,
            pages=180,
            description='A classic novel about ambition, wealth, love, and loss.',
        ),
        Book(
            title='Sapiens',
            author='Yuval Noah Harari',
            category='History',
            image_url='/book_house.png',
            rating=4.6,
            year=2011,
            pages=443,
            description='A history book about the development of humans and societies.',
        ),
        Book(
            title='Rich Dad Poor Dad',
            author='Robert Kiyosaki',
            category='Business',
            image_url='/land2.jpg',
            rating=4.5,
            year=1997,
            pages=336,
            description='A personal finance book about money mindset and investing basics.',
        ),
        Book(
            title='Deep Work',
            author='Cal Newport',
            category='Self Help',
            image_url='/land3.jpg',
            rating=4.7,
            year=2016,
            pages=304,
            description='A book about focus, concentration, and doing valuable work without distraction.',
        ),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_books, migrations.RunPython.noop),
    ]
