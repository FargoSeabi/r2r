from django.core.management.base import BaseCommand
from villages.models import Village
from marketplace.models import Entrepreneur, Product
from training.models import TrainingModule
import uuid


class Command(BaseCommand):
    help = 'Seed database with South African tribal village data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding South African tribal village data...')
        
        # Create villages
        villages_data = [
            {
                'name': 'Shakaland Zulu Village',
                'description': 'Experience authentic Zulu traditions, spear-making demonstrations, traditional ceremonies, and the warrior culture that shaped South African history.',
                'country': 'South Africa',
                'region': 'KwaZulu-Natal',
                'category': 'rituals',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200',
                    'https://images.unsplash.com/photo-1571217297629-dee4e90e3c7d?w=1200'
                ],
                'rating': 4.8,
                'visit_count': 245,
                'experience_duration': 120
            },
            {
                'name': 'Langa Xhosa Cultural Village',
                'description': 'Discover Xhosa customs, click-language demonstrations, beadwork artistry, and Nelson Mandela heritage in this vibrant township.',
                'country': 'South Africa', 
                'region': 'Western Cape',
                'category': 'crafts',
                'image_url': 'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=1200',
                    'https://images.unsplash.com/photo-1566069740273-26c0b6c63318?w=1200'
                ],
                'rating': 4.7,
                'visit_count': 189,
                'experience_duration': 90
            },
            {
                'name': 'Mafikeng Tswana Heritage Site',
                'description': 'Learn traditional Tswana pottery, explore the birthplace of Ubuntu philosophy, and experience authentic setswana music and dance.',
                'country': 'South Africa',
                'region': 'North West Province', 
                'category': 'music',
                'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200',
                    'https://images.unsplash.com/photo-1571217297629-dee4e90e3c7d?w=1200'
                ],
                'rating': 4.6,
                'visit_count': 156,
                'experience_duration': 100
            },
            {
                'name': 'Golden Gate Sotho Village',
                'description': 'Experience Basotho mountain culture, traditional blanket weaving, sorghum beer brewing, and horseback riding through spectacular highlands.',
                'country': 'South Africa',
                'region': 'Free State',
                'category': 'crafts',
                'image_url': 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1200',
                    'https://images.unsplash.com/photo-1566069740273-26c0b6c63318?w=1200'
                ],
                'rating': 4.5,
                'visit_count': 134,
                'experience_duration': 150
            },
            {
                'name': 'Mpumalanga Ndebele Village',
                'description': 'Marvel at vibrant geometric wall paintings, traditional house decorating, geometric beadwork, and colorful Ndebele clothing traditions.',
                'country': 'South Africa',
                'region': 'Mpumalanga',
                'category': 'crafts',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200',
                    'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=1200'
                ],
                'rating': 4.9,
                'visit_count': 178,
                'experience_duration': 85
            },
            {
                'name': 'Limpopo Venda Sacred Sites',
                'description': 'Explore ancient Venda spiritual traditions, sacred forest ceremonies, traditional drumming, and the mystical Lake Fundudzi.',
                'country': 'South Africa',
                'region': 'Limpopo',
                'category': 'rituals',
                'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',
                'vr_images': [
                    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200',
                    'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1200'
                ],
                'rating': 4.7,
                'visit_count': 167,
                'experience_duration': 110
            }
        ]

        villages = []
        for village_data in villages_data:
            village, created = Village.objects.get_or_create(
                name=village_data['name'],
                defaults=village_data
            )
            villages.append(village)
            if created:
                self.stdout.write(f'Created village: {village.name}')

        # Create entrepreneurs
        entrepreneurs_data = [
            {
                'name': 'Nomsa Zulu',
                'email': 'nomsa@shakaland.co.za',
                'location': 'KwaZulu-Natal, South Africa',
                'biography': 'Master Zulu beadwork artisan and cultural storyteller. Nomsa preserves ancient Zulu traditions through intricate beadwork that tells stories of lineage, love, and Ubuntu values.',
                'profile_image_url': 'https://images.unsplash.com/photo-1494790108755-2616c6fd6215?w=400',
                'village': villages[0],  # Shakaland Zulu Village
                'specialties': ['Zulu beadwork', 'Traditional ceremonies', 'Cultural storytelling'],
                'monthly_income': 1200.00,
                'families_supported': 3,
                'is_verified': True
            },
            {
                'name': 'Thandiwe Mbeki',
                'email': 'thandiwe@langa.co.za', 
                'location': 'Western Cape, South Africa',
                'biography': 'Xhosa textile artist specializing in traditional blankets and modern African fashion. Thandiwe bridges ancestral techniques with contemporary design.',
                'profile_image_url': 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400',
                'village': villages[1],  # Langa Xhosa Cultural Village
                'specialties': ['Xhosa textiles', 'Traditional blankets', 'African fashion'],
                'monthly_income': 980.00,
                'families_supported': 2,
                'is_verified': True
            },
            {
                'name': 'Kgomotso Mokoena',
                'email': 'kgomotso@mafikeng.co.za',
                'location': 'North West Province, South Africa', 
                'biography': 'Tswana pottery master and Ubuntu philosophy teacher. Kgomotso creates traditional clay vessels while teaching cooperative business principles.',
                'profile_image_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400',
                'village': villages[2],  # Mafikeng Tswana Heritage Site
                'specialties': ['Traditional pottery', 'Ubuntu principles', 'Community cooperation'],
                'monthly_income': 850.00,
                'families_supported': 4,
                'is_verified': True
            },
            {
                'name': 'Palesa Mthembu',
                'email': 'palesa@goldgate.co.za',
                'location': 'Free State, South Africa',
                'biography': 'Basotho blanket weaver and traditional food specialist. Palesa creates authentic Basotho blankets and traditional sorghum products.',
                'profile_image_url': 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400',
                'village': villages[3],  # Golden Gate Sotho Village
                'specialties': ['Basotho blankets', 'Traditional weaving', 'Sorghum products'],
                'monthly_income': 1100.00,
                'families_supported': 2,
                'is_verified': True
            }
        ]

        entrepreneurs = []
        for entrepreneur_data in entrepreneurs_data:
            entrepreneur, created = Entrepreneur.objects.get_or_create(
                email=entrepreneur_data['email'],
                defaults=entrepreneur_data
            )
            entrepreneurs.append(entrepreneur)
            if created:
                self.stdout.write(f'Created entrepreneur: {entrepreneur.name}')

        # Create products
        products_data = [
            {
                'name': 'Authentic Zulu Love Letter Beadwork',
                'description': 'Traditional Zulu courtship beadwork telling stories of love and family heritage. Each pattern carries deep cultural meaning and Ubuntu values.',
                'price': 45.00,
                'category': 'handcrafts',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500',
                'entrepreneur': entrepreneurs[0],
                'is_experience': False,
                'availability': 15,
                'tags': ['Zulu', 'beadwork', 'traditional', 'handmade', 'South African']
            },
            {
                'name': 'Premium South African Biltong Selection',
                'description': 'Authentic air-dried biltong made using traditional Afrikaner methods. A taste of South African heritage in every bite.',
                'price': 28.00,
                'category': 'food',
                'image_url': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500',
                'entrepreneur': entrepreneurs[0],
                'is_experience': False,
                'availability': 50,
                'tags': ['biltong', 'traditional food', 'South African', 'dried meat']
            },
            {
                'name': 'Traditional Xhosa Blanket Weaving',
                'description': 'Authentic Xhosa blankets handwoven using ancestral techniques. Each blanket represents cultural identity and Ubuntu community values.',
                'price': 120.00,
                'category': 'textiles',
                'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500',
                'entrepreneur': entrepreneurs[1],
                'is_experience': False,
                'availability': 8,
                'tags': ['Xhosa', 'blanket', 'weaving', 'traditional', 'handmade']
            },
            {
                'name': 'Rooibos Tea & Honeybush Collection',
                'description': 'Premium South African rooibos and honeybush tea blend. Caffeine-free herbal teas from the Cederberg mountains.',
                'price': 18.00,
                'category': 'food',
                'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500',
                'entrepreneur': entrepreneurs[1],
                'is_experience': False,
                'availability': 35,
                'tags': ['rooibos', 'honeybush', 'tea', 'South African', 'herbal']
            },
            {
                'name': 'Tswana Pottery Ubuntu Workshop Experience',
                'description': 'Learn traditional Tswana pottery techniques while exploring Ubuntu philosophy and community cooperation principles.',
                'price': 65.00,
                'category': 'experiences',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500',
                'entrepreneur': entrepreneurs[2],
                'is_experience': True,
                'duration': 180,
                'availability': 12,
                'tags': ['pottery', 'Ubuntu', 'workshop', 'Tswana', 'traditional']
            },
            {
                'name': 'Authentic Basotho Heritage Blanket',
                'description': 'Traditional Basotho blankets from the mountain kingdom. Each blanket represents cultural identity and protection from mountain weather.',
                'price': 95.00,
                'category': 'textiles',
                'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500',
                'entrepreneur': entrepreneurs[3],
                'is_experience': False,
                'availability': 10,
                'tags': ['Basotho', 'blanket', 'traditional', 'mountain', 'heritage']
            },
            {
                'name': 'Traditional Bobotie Cooking Experience',
                'description': 'Learn to cook authentic South African bobotie with traditional spices and techniques. Includes recipe and cultural history.',
                'price': 55.00,
                'category': 'experiences',
                'image_url': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500',
                'entrepreneur': entrepreneurs[3],
                'is_experience': True,
                'duration': 150,
                'availability': 8,
                'tags': ['bobotie', 'cooking', 'South African cuisine', 'traditional', 'experience']
            },
            {
                'name': 'Sorghum Beer Traditional Brewing',
                'description': 'Traditional South African sorghum beer made using ancestral fermentation methods. A cultural taste experience.',
                'price': 22.00,
                'category': 'food',
                'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500',
                'entrepreneur': entrepreneurs[2],
                'is_experience': False,
                'availability': 20,
                'tags': ['sorghum beer', 'traditional', 'fermented', 'South African', 'cultural']
            }
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                entrepreneur=product_data['entrepreneur'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create training modules
        training_modules_data = [
            {
                'title': 'Ubuntu Digital Business Principles',
                'description': 'Learn how traditional Ubuntu philosophy applies to modern digital business practices, emphasizing community cooperation and shared prosperity.',
                'category': 'ubuntu-principles',
                'difficulty': 'beginner',
                'duration': 45,
                'video_url': 'https://example.com/ubuntu-business',
                'material_urls': ['https://example.com/ubuntu-guide.pdf']
            },
            {
                'title': 'Digital Marketing for African Artisans',
                'description': 'Master social media marketing, online storytelling, and digital brand building specifically for traditional African crafts and cultural products.',
                'category': 'marketing',
                'difficulty': 'intermediate',
                'duration': 90,
                'video_url': 'https://example.com/digital-marketing',
                'material_urls': ['https://example.com/marketing-guide.pdf', 'https://example.com/social-media-templates.zip']
            },
            {
                'title': 'E-commerce for Rural Communities',
                'description': 'Build online stores, manage inventory, process payments, and handle shipping for rural and traditional businesses.',
                'category': 'ecommerce',
                'difficulty': 'intermediate',
                'duration': 120,
                'video_url': 'https://example.com/ecommerce-rural',
                'material_urls': ['https://example.com/ecommerce-setup.pdf']
            },
            {
                'title': 'Digital Literacy for Traditional Artisans',
                'description': 'Basic computer skills, internet navigation, email communication, and digital photography for showcasing traditional crafts.',
                'category': 'digital-literacy',
                'difficulty': 'beginner',
                'duration': 60,
                'video_url': 'https://example.com/digital-literacy',
                'material_urls': ['https://example.com/computer-basics.pdf']
            },
            {
                'title': 'Community Cooperative Digital Models',
                'description': 'Learn how to establish digital cooperatives based on Ubuntu principles, sharing resources and profits within traditional communities.',
                'category': 'ubuntu-principles',
                'difficulty': 'advanced',
                'duration': 150,
                'video_url': 'https://example.com/cooperative-models',
                'material_urls': ['https://example.com/cooperative-guide.pdf', 'https://example.com/legal-framework.pdf']
            }
        ]

        for module_data in training_modules_data:
            module, created = TrainingModule.objects.get_or_create(
                title=module_data['title'],
                defaults=module_data
            )
            if created:
                self.stdout.write(f'Created training module: {module.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded South African tribal village data!')
        )