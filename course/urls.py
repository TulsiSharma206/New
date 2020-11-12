from django.urls import path
from .views import CourseCreate, CourseRU, DeleteCourse, FileList, FileUploadss, PurchaseCreate, PurchaseRU, DeletePurchase, MyCourse, CountRU, myChapter, myChaptervideo, mycurrentvideo, myvideocurr, mypvideo, allVideoTime, allcourse, coursechapter, mediauploading, purcahaseget, Chaptervideo, MockAnswerList, MockSubmitAnswer, MockScore, AssignmentsList, AssignmentsSubmitAnswer, AssignmentsScore, allmock, mockpercentage, assegmentpercentage
from django.contrib.auth import views
#from django.views.decorators.csrf import csrf_exempt 

urlpatterns = [
	path('coursecreate/', CourseCreate.as_view(),name="All course List"),
	path('course/<pk>/', CourseRU.as_view(), name='get Course'),
	path("coursedeleted/<pk>/", DeleteCourse.as_view()),

	path("fileuploadss/", FileUploadss.as_view({'get': 'list', 'post' : 'create'}), name="upload video in our course"),
	
	path("listvideo/<pk>/", FileList, name="particular course all videos"),

	path('purcahse/', PurchaseCreate,name="All course List"),
	path('purchase/<pk>/', PurchaseRU.as_view(), name='get Course'),
	path("purchasedeleted/<pk>/", DeletePurchase.as_view()),

	path("mycourse/", MyCourse, name="My all course"),

	path("watch/<pk>/", CountRU, name="count watch video"),

	path("chapterss/<pk>/", myChapter, name="current user all chapter"),

	path("mychaptervideo/<pk>/", myChaptervideo, name="particular chapter video"),

	path("lastplay/<pk>/", mycurrentvideo, name="userlastpaly Video"),

	path("myvideocurr/<pk>/", myvideocurr, name="user  lastpaly Video"),

	path("mypvideo/<pk>/", mypvideo, name="user  lastpaly Video"),

	path("allvideotime/<pk>/", allVideoTime, name="user  all video time"),

	path("allcourse/", allcourse, name="All Courses"),
	path("chapterp/<pk>/", coursechapter, name="Particular chapter"),

	path("mediaupload/", mediauploading, name="Video upload using html"),

	path("purcahaseget/", purcahaseget, name="purcase html"),

	path("chaptervideo/<pk>/", Chaptervideo, name="chapter video"),
		
	path('manswer/', MockAnswerList,name="All Mock Answer"),
	path('msubmitanswer/<pk>/<cpk>/', MockSubmitAnswer,name="Mock submit Answer"),
	path('mscore/<pk>/', MockScore,name="mock score"),

	path('assanswer/', AssignmentsList,name="All Assignemnets Answer"),
	path('asssubmitanswer/<cpk>/<pk>/', AssignmentsSubmitAnswer,name="Assignments submit Answer"),
	path('assscore/<pk>/', AssignmentsScore,name="assignments score"),

	path('mock/', allmock, name="all mock list"),

	path('mockpercen/', mockpercentage, name="mock percentage"),

	path('assepercen/', assegmentpercentage, name="mock percentage"),
]


