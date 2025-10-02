from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми продуктами и категориями'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        self.stdout.write('Удаление старых данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS('Старые данные успешно удалены!')
        )

        # Создаем категории
        self.stdout.write('Создание категорий...')

        categories_data = [
            {
                'name': 'Электроника',
                'description': 'Техника и гаджеты'
            },
            {
                'name': 'Одежда',
                'description': 'Одежда и аксессуары'
            },
            {
                'name': 'Книги',
                'description': 'Книги и учебники'
            },
            {
                'name': 'Для дома',
                'description': 'Товары для дома'
            },
            {
                'name': 'Спорт',
                'description': 'Спортивные товары'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description']
            )
            categories[cat_data['name']] = category
            self.stdout.write(f'  Создана категория: {cat_data["name"]}')

        # Создаем продукты
        self.stdout.write('Создание продуктов...')

        products_data = [
            {
                'name': 'iPhone 15',
                'description': 'Новый смартфон с улучшенной камерой',
                'price': 999.99,
                'category': 'Электроника'
            },
            {
                'name': 'MacBook Pro',
                'description': 'Мощный ноутбук для работы и творчества',
                'price': 1999.99,
                'category': 'Электроника'
            },
            {
                'name': 'Наушники беспроводные',
                'description': 'Качественные наушники с шумоподавлением',
                'price': 199.99,
                'category': 'Электроника'
            },
            {
                'name': 'Футболка хлопковая',
                'description': 'Комфортная футболка из 100% хлопка',
                'price': 29.99,
                'category': 'Одежда'
            },
            {
                'name': 'Джинсы классические',
                'description': 'Удобные джинсы прямого кроя',
                'price': 79.99,
                'category': 'Одежда'
            },
            {
                'name': 'Кроссовки спортивные',
                'description': 'Легкие кроссовки для бега и фитнеса',
                'price': 89.99,
                'category': 'Одежда'
            },
            {
                'name': 'Изучаем Python',
                'description': 'Лучшая книга для начинающих программистов',
                'price': 49.99,
                'category': 'Книги'
            },
            {
                'name': 'Django для профессионалов',
                'description': 'Продвинутая книга по веб-разработке',
                'price': 59.99,
                'category': 'Книги'
            },
            {
                'name': 'Кофеварка',
                'description': 'Автоматическая кофеварка для дома',
                'price': 149.99,
                'category': 'Для дома'
            },
            {
                'name': 'Фитнес-браслет',
                'description': 'Умный браслет для отслеживания активности',
                'price': 79.99,
                'category': 'Спорт'
            },
            {
                'name': 'Йога-мат',
                'description': 'Профессиональный коврик для йоги',
                'price': 39.99,
                'category': 'Спорт'
            },
            {
                'name': 'Велосипед горный',
                'description': 'Надежный горный велосипед для активного отдыха',
                'price': 499.99,
                'category': 'Спорт'
            }
        ]

        for product_data in products_data:
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=categories[product_data['category']]
            )
            self.stdout.write(f'  Создан продукт: {product_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {Category.objects.count()} категорий и '
                f'{Product.objects.count()} продуктов!'
            )
        )