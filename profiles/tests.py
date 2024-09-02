from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile, Company, Label
from profiles.serializer import ProfileListOrderingEnum, ProfileDetailSerializer

class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.company1 = Company.objects.create(id=1,name="Company 1")
        self.company2 = Company.objects.create(id=2,name="Company 2")
        self.company3 = Company.objects.create(id=3,name="Company 3")
        
        self.profile1 = Profile.objects.create(
            img_url='http://example.com/img1.jpg', 
            name='테스트입니다.', 
            email='abcd@example.com', 
            tel='010-1234-5678', 
            rank='부장', 
            address='서울시 강남구', 
            birthday='1990-05-15', 
            web_site='http://www.example.com', 
            memo='메모 1', 
            company=self.company1
        )
        Label.objects.create(name='테스트 라벨 1', profile=self.profile1)
        Label.objects.create(name='테스트 라벨 2', profile=self.profile1)
        
        self.profile2 = Profile.objects.create(
            img_url='http://example.com/img2.jpg', 
            name='안녕하세요.', 
            email='pure@example.com', 
            tel='010-9876-5432', 
            rank='엔지니어', 
            address='서울시 종로구', 
            birthday='1988-10-20', 
            memo='메모 2', 
            company=self.company1
        )
        Label.objects.create(name='테스트 라벨 3', profile=self.profile2)
        Label.objects.create(name='테스트 라벨 4', profile=self.profile2)
        
        self.profile3 = Profile.objects.create(
            img_url='http://example.com/img3.jpg', 
            name='반갑습니다.', 
            email='red@example.com', 
            tel='010-5555-7777', 
            rank='사원', 
            address='부산시 해운대구', 
            birthday='1995-03-25', 
            web_site='http://www.example.com', 
            memo='메모 3', 
            company=self.company2
        )
        Label.objects.create(name='테스트 라벨 5', profile=self.profile3)
        
        self.profile4 = Profile.objects.create(
            img_url='http://example.com/img4.jpg', 
            name='가나다라', 
            email='blue@example.com', 
            tel='010-9999-9999', 
            rank='매니저', 
            birthday='1985-07-12', 
            memo='메모 4', 
            company=self.company2
        )
        Label.objects.create(name='테스트 라벨 6', profile=self.profile4)

        self.profile5 = Profile.objects.create(
            img_url='http://example.com/img5.jpg', 
            name='가나다라23', 
            email='zzz@example.com', 
            tel='010-1111-1111', 
            rank='사원', 
            birthday='1990-01-01', 
            memo='메모 5', 
            company=self.company3
        )

    def test_profile_list_view_ordering_success(self):
        url = reverse('profile_list')
        
        # 이름 오름차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.NAME_ASC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], '가나다라')
        
        # 이름 내림차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.NAME_DESC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], '테스트입니다.')
        
        # 이메일 오름차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.EMAIL_ASC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['email'], 'abcd@example.com')
        
        # 이메일 내림차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.EMAIL_DESC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['email'], 'zzz@example.com')
        
        # 전화번호 오름차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.TEL_ASC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['tel'], '010-1111-1111')
        
        # 전화번호 내림차순 검증
        response = self.client.get(url, {'ordering': ProfileListOrderingEnum.TEL_DESC})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['tel'], '010-9999-9999')
        

    def test_profile_list_view_pagination_success(self):
        url = reverse('profile_list')
        
        # 2개씩 데이터 분할 페이지네이션 검증
        response = self.client.get(url, {'page_size': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # 3개씩 데이터 분할 페이지네이션 검증
        response = self.client.get(url, {'page_size': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        
        # 4개씩 데이터 분할 페이지네이션 검증
        response = self.client.get(url, {'page_size': 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        
        # 5개씩 데이터 분할 페이지네이션 검증
        response = self.client.get(url, {'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)


    def test_profile_list_ordering_enum_invalid_data(self):
        url = reverse('profile_list')
        
        # ordering enum invalid data 검증
        response = self.client.get(url, {'ordering': 'invalid_data'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    # 올바른 프로필 상세 검증
    def test_profile_detail_view_success(self):
        url = reverse('profile_detail')
        
        response = self.client.get(url, {'id': self.profile1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = ProfileDetailSerializer(instance=self.profile1)
        self.assertEqual(response.data['img_url'], serializer.data['img_url'])
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['memo'], serializer.data['memo'])
    
    
    # 올바르지 않은 프로필 상세 검증
    def test_profile_detail_not_found(self):
        url = reverse('profile_detail')
        
        response = self.client.get(url, {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 올바른 프로필 생성 검증
    def test_create_valid_profile(self):
        url = reverse('profile_create')
        
        valid_payload = {
            'img_url': 'http://example.com/img.jpg',
            'name':'테스트',
            'email': 'test@example.com',
            'tel': '010-1234-5678',
            'rank': '매니저',
            'address': '테스트 데이터',
            'birthday': '1990-01-01',
            'web_site': 'http://www.example.com',
            'memo': 'Test memo',
            'company_id': 1,
            'labels': ['Label 1', 'Label 2']
        }
        
        response = self.client.post(url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], valid_payload['name'])
        self.assertEqual(response.data['email'], valid_payload['email'])
        self.assertEqual(response.data['memo'], valid_payload['memo'])
        self.assertEqual(response.data['rank'], valid_payload['rank'])
    
    # 올바르지 않은 프로필 생성 검증
    def test_create_invalid_profile(self):
        invalid_payload = {
            'img_url': 'http://example.com/img.jpg',
            'name': '테스트2',
            'email': 'test@example.com',
            'tel': '010-1234-5678',
            'rank': '매니저',
            'address': '테스트',
            'birthday': '1990-01-01',
            'web_site': 'http://www.example.com',
            'memo': 'Test memo',
            'company_id': 999,
            'labels': ['Label 1', 'Label 2']
        }
        url = reverse('profile_create')
        
        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('company_id', response.data)
        self.assertEqual(response.data['company_id'][0], "Company does not exist")