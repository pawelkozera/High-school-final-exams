from django.urls import include, path
from rest_framework import routers
from . import views
from .views import QuestionViewSet

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'groups', views.GroupViewSet)

app_name = 'pytania'
urlpatterns = [
	path('', views.index, name='index'),
	path('zawodowe', views.index_zawodowy, name='index_zawodowy'),
	path('pytanie/<str:group_name>', views.question_options, name='question_options'),
	path('pytanie/<str:group_name>/liczba_pytan', views.random_test_number_selecting, name='random_test_number_selecting'),
	path('pytanie/pojedyncze/<int:random_question_id>', views.next_question_display, name='next_question_display'),
	path('pytanie/<str:group_name>/pojedyncze', views.question_display, name='question_display'),
	path('pytanie/<str:group_name>/test/<str:test_type>/<int:number_of_questions>', views.generated_test, name='generated_test'),
	path('pytanie/<str:group_name>/wybor', views.test_selecting, name='test_selecting'),
	path('contact', views.contact, name='contact'),
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]