from rest_framework import generics, pagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

from profiles.models import Profile
from profiles.serializer import (
    ProfileOrderingSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer,
    ProfileCreateSerializer,
    ProfileListOrderingEnum
)

class ProfileListPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100 

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                description="정렬 순서",
                type=openapi.TYPE_STRING,
                enum=[e.value for e in ProfileListOrderingEnum],
            )
        ]
    ),
)
class ProfileListView(generics.ListAPIView):
    """
    프로필 목록
    
    # Author
    - 원재연
    
    # Request Query Parameter
    - page : int = 원하는 페이지
    - page_size : int = 각 페이지당 원하는 데이터 사이즈
    - ordering : Enum (아래 선택지 중 택1) [Optional]
        - name : 이름 오름차순
        - -name : 이름 내림차순
        - email : 이메일 오름차순
        - -email : 이메일 내림차순
        - tel : 전화번호 오름차순
        - -tel : 전화번호 내림차순
        
    # Response
    ```
    {
        "count": int = 총 데이터 갯수,
        "next": string = 다음 페이지 url (없을 시 null Response),
        "previous": string = 이전 페이지 url (없을 시 null Response),
        "results": [
            {
                "id": int = 프로필 고유 ID,
                "img_url": string = 프로필 이미지,
                "name": string = 이름,
                "email": string = 이메일,
                "tel": string = 전화번호,
                "rank": string = 직급,
                "company_id": int = 회사 고유 ID,
                "company_name": string = 회사명,
                "labels": list[str] = 라벨 (없을 시, 빈 리스트)
            }
        ]
    }
    ```
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    pagination_class = ProfileListPagination
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('company')
        
        serializer = ProfileOrderingSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        ordering = serializer.validated_data.get('ordering', None)
        
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="프로필 id",
                type=openapi.TYPE_INTEGER
            )
        ]
    ),
)
class ProfileDetailView(generics.RetrieveAPIView):
    """
    프로필 상세 조회
    
    # Author
    - 원재연
    
    # Request Query Parameter
    - id : 프로필 id
        
    # Response
    ```
    {
        "id": int = 프로필 고유 ID,
        "img_url": string = 프로필 이미지,
        "name": string = 이름,
        "email": string = 이메일,
        "tel": string = 전화번호,
        "rank": string = 직급,
        "company_id": int = 회사 고유 ID,
        "company_name": string = 회사명,
        "labels": list[str] = 라벨 (없을 시, 빈 리스트),
        "memo": string = 메모 (없을 시, null),
        "address": string = 주소 (없을 시, null),
        "birthday": string = 생년월일 (없을 시, null),
        "web_site": string = 웹사이트 (없을 시, null)
    }
    ```
    """
    serializer_class = ProfileDetailSerializer  

    def get_object(self):
        id = self.request.query_params.get('id')
        
        profile = generics.get_object_or_404(Profile, id=id)
        return profile


class ProfileCreateView(generics.CreateAPIView):
    """
    프로필 생성
    
    # Author
    - 원재연
    
    # Request Body
    - img_url = 프로필 이미지 (string)
    - name = 이름 (string)
    - email = 이메일 (string)
    - tel = 전화번호 (string)
    - rank = 직급 (string)
    - company_id = 회사 id (int)
    - address = 주소 (Optional) (string)
    - birthday = 생년월일 (Optional) (string)
    - web_site = 웹사이트 (Optional) (string)
    - labels = 라벨 (Optional) (list[string])
        
    # Response
    ```
    {
        "id": int = 프로필 고유 ID,
        "img_url": string = 프로필 이미지,
        "name": string = 이름,
        "email": string = 이메일,
        "tel": string = 전화번호,
        "rank": string = 직급,
        "company_id": int = 회사 고유 ID,
        "company_name": string = 회사명,
        "labels": list[str] = 라벨 (없을 시, 빈 리스트),
        "memo": string = 메모 (없을 시, null),
        "address": string = 주소 (없을 시, null),
        "birthday": string = 생년월일 (없을 시, null),
        "web_site": string = 웹사이트 (없을 시, null)
    }
    ```
    """
    serializer_class = ProfileCreateSerializer