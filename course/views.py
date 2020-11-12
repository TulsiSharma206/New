from rest_framework import generics
from .serializers import CourseSerializer, FileUploadSerializer, PurchaseSerializer, CountSerializer, CurrentVideoSerializer #  assignmentSerializer,
from .models import Course, FileUpload, Purchase, assignments, Count, CurrentVideo, Chapter, MockTestProgress, MockTest,MockTestPercentage,AssignmentsTest,AssignmentsProgress,AssignmentsPercentage, NumberofMock
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from user.models import User 
import os
from mcquestions.models import NumberOfQuestions


# All Course Show user login or not and puchase or not all Course show 
class CourseCreate(generics.ListCreateAPIView):
    queryset = Course.objects.filter(status=True)
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseRU(generics.RetrieveUpdateAPIView):
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs['pk'])


class DeleteCourse(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    def get_queryset(self):
        user_v = Course.objects.get(id=self.kwargs['pk'],user=self.request.user).delete()
        return Course.objects.all()


# All Mycourse Show (Done)
@csrf_exempt
@api_view(["POST", "GET"])
def MyCourse(request):
    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid=Token.objects.get(key=t)
        user=int(userid.user.id)
        serializer_class = CourseSerializer
        if userid.user.id is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'), status= True).values('id', 'title','image'))
    except ObjectDoesNotExist:
        return Response({"Fail": "Session Logout"})


# List Particular Course all Video
@csrf_exempt
@api_view(["GET"])
def FileList(request,pk):
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    user=int(userid.user.id)
    if user is None:
        return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            Course.objects.get(id__in=Purchase.objects.filter(purchaseuser=userid.user))
            data = FileUpload.objects.filter(courses=Course.objects.get(id=pk)).values('id','image','url')
            return Response ({"data": data})
            # return Response(FileUpload.objects.filter(courses=Course.objects.get(id=pk)).values('id','image','uploadfile'))#.values('image','uploadfile')
        except ObjectDoesNotExist:
            return Response({"Fail": "Please Purchase First this course"}, status=status.HTTP_400_BAD_REQUEST)
        

class PurchaseRU(generics.RetrieveUpdateAPIView):
    serializer_class = PurchaseSerializer
    def get_queryset(self):
        return Purchase.objects.filter(id=self.kwargs['pk'])


class DeletePurchase(generics.RetrieveAPIView):
    serializer_class = PurchaseSerializer
    def get_queryset(self):
        user_v = Purchase.objects.get(id=self.kwargs['pk']).delete()
        return Purchase.objects.all()


@csrf_exempt
@api_view(["POST","GET"])
def CountRU(request,pk):
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    user=int(userid.user.id)
    if user is None:
        return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            watch_vi = Count.objects.get(mediafile=FileUpload.objects.get(id=pk),user=userid.user) #request.data.get('id')
            print("watch_vi",watch_vi)
            if request.method == 'POST':
                #import pdb;pdb.set_trace()
                watch_vi.watch = watch_vi.watch + 1
                if request.data.get('complete') == "True":
                    watch_vi.is_complete = True
                else:
                    pass
                watch_vi.save()
                return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk),user=userid.user).values('watch', 'is_complete')) 
            else:
                return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk),user=userid.user).values('watch', 'is_complete'))
        except ObjectDoesNotExist:
            #import pdb;pdb.set_trace()
            is_status = False
            if request.data.get('complete') == "True":
                is_status = True
            else:
                pass
            Count.objects.create(mediafile=FileUpload.objects.get(id=pk),user=User.objects.get(id=user),is_complete=is_status)
            return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk), user=userid.user).values('watch', 'is_complete'))


@csrf_exempt
@api_view(["POST","GET"])
def allVideoTime(request,pk):
    t = request.META['HTTP_AUTHORIZATION']
    userid=Token.objects.get(key=t)
    user=int(userid.user.id)
    if user is None:
        return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            mediat = Count.objects.get(mediafile=FileUpload.objects.get(id=pk),user=userid.user) 
            if request.method == 'POST':
                mediat.vtime = request.data.get('vtime')
                mediat.save()
                return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk),user=userid.user).values('vtime', 'mediafile_id'))
            else:
                return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk),user=userid.user).values('vtime', 'mediafile_id'))
        except ObjectDoesNotExist:
            Count.objects.create(mediafile=FileUpload.objects.get(id=pk),user=User.objects.get(id=user),vtime = request.data.get('vtime'))
            return Response(Count.objects.filter(mediafile=FileUpload.objects.get(id=pk),user=userid.user).values('vtime', 'mediafile_id'))


def Tokens(tok):
    try:
        token=Token.objects.get(key=tok)
        return token
    except ObjectDoesNotExist:
        return None


# POst method of user play last video and play last durations time pk=chapterid
@csrf_exempt
@api_view(["POST"])
def mycurrentvideo(request,pk): # Pk Course id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    if userid != None:
        userv=userid.user.id
        try:
            #import pdb;pdb.set_trace()
            current_video = CurrentVideo.objects.get(user=User.objects.get(id=userv),coures=Course.objects.get(id=pk))
            current_video.currenv_id = int(request.data.get('currenv'))
            current_video.time = request.data.get('time')
            current_video.save()
            return Response({'status': "successfuly"})
        except ObjectDoesNotExist:
            #import pdb;pdb.set_trace()
            CurrentVideo.objects.create(user=User.objects.get(id=userv),coures=Course.objects.get(id=pk),currenv=FileUpload.objects.get(id=request.data.get('currenv')),time = request.data.get('time'))
            return Response({'status': "successfuly Create"})
    else:
        return Response({'status': "please login First"})


# Particular Course all Chapter
@csrf_exempt
@api_view(["POST","GET"])
def myChapter(request,pk): # Pk Course id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    if userid != None:
        userv=userid.user.id
        if userv is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            purchaseChapter = Chapter.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, cours_id=pk ,status=True).values('chapter_id')).values('id','title', 'course_id')
            # allChapter = Chapter.objects.filter(course=pk).values('id', 'title')
            return Response({'purchaseChapter': purchaseChapter, 'courseid' : pk}) # ,'allChapter' : allChapter
    else:
        return Response({'status': "please login First"})


# Particular Chapter all Videos
@csrf_exempt
@api_view(["POST","GET"])
def myChaptervideo(request,pk): # Pk chapter id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    if userid != None:
        userv=userid.user.id
        if userv is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # current_video = CurrentVideo.objects.filter(user=User.objects.get(id=userv),cours=Chapter.objects.get(id=pk)).values('currenv', 'time')
            Chaptervideos = FileUpload.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, chapter_id=pk ,status=True).values('media')).values('id','name')#.values('id', "uploadfile", "image")
            return Response({'Chaptervideos': Chaptervideos}) 
    else:
        return Response({'status': "please login First"})


# First Time only one video second time Current Video
@csrf_exempt
@api_view(["GET"])
def myvideocurr(request,pk): # Pk Course id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    if userid != None:
        userv=userid.user.id
        current_video = CurrentVideo.objects.filter(user_id=userv,coures_id=pk).values('currenv', 'time')
        if len(current_video) != 0 :
            currebtdata = FileUpload.objects.filter(id__in=current_video.values('currenv')).values('id','name', "url","image")
            watchcount = Count.objects.filter(mediafile__in=currebtdata.values('id'), user_id=userv).values('mediafile', 'watch')
            try:
                data = Count.objects.get(mediafile__in=currebtdata.values('id'), user_id=userv)
            except ObjectDoesNotExist:
                data = Count.objects.create(mediafile_id=currebtdata.values('id'), user_id=userv)
            datac = currebtdata.values('id')[0]
            if data.watch >=4:
                Chaptervideos = FileUpload.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, cours_id=pk ,status=True).values('media')).values('id')
                z=0
                for i in Chaptervideos:
                    if i == datac:
                        break
                    else:
                        z=z+1
               # import pdb;pdb.set_trace()
                if len(Chaptervideos) > (z+1):
                    try:
                        n=Chaptervideos[z+1]
                        m=str(n)
                        f=m.find(":")
                        l=m.find("}")
                        m=m[f+1:l]
                    except IndexError:
                        countdata = Count.objects.filter(user_id=userv).values('mediafile_id')
                        j = []
                        for i in range(0,len(countdata)):
                            j.append(countdata[i]['mediafile_id'])
                        Chapt = FileUpload.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, cours_id=pk ,status=True).values('media')).values('id')
                        k=[]
                        for i in range(0,len(Chapt)):
                            k.append(Chapt[i]['id'])
                        l = set(k) - set(j)
                        ls = list(l)
                        ls = ls[0]
                        if len(l) != 0:
                            m=ls
                        else:
                            return Response({'currebtdata': "You Complete all videos"})

                    Chaptervideos = FileUpload.objects.filter(id=m).values('id', 'name',"url", "image")
                    current_video = {
                        "id" : 0,
                        "currenv" : 0,
                        "time"   :  0
                    }
                    watchcount = {
                        "id" : 0,
                        "mediafile" : 0,
                        "watch"   :  0
                    }
                else:
                    return Response({'currebtdata': "You Complete all videos"})
                return Response({'currebtdata': Chaptervideos, "current_video":[current_video], "watchcount" : [watchcount]})
            else:
                return Response({'currebtdata': currebtdata, 'current_video' : current_video, "watchcount": watchcount})
        else:
            try:
                Chaptervideos = FileUpload.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user, cours_id=pk ,status=True).values('media')).values('id', 'name',"url", "image")[0]
            except IndexError:
                return Response({'Chaptervideos': "You complete all video please purchase again"})
            current_video = {
                    "id" : 0,
                    "currenv" : 0,
                    "time"   :  0
                }
            watchcount = {
                "id" : 0,
                "mediafile" : 0,
                "watch"   :  0
            }
            return Response({'currebtdata':[Chaptervideos], "current_video":[current_video], "watchcount" : [watchcount]}) 
    else:
        return Response({'status': "please login First"})




# Particular Video id get
@csrf_exempt 
@api_view(["GET"])
def mypvideo(request,pk): # Pk Video id
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    if userid != None:
        userv=userid.user.id
        Chaptervideos = Purchase.objects.filter(purchaseuser=userid.user, status=True,media__in= FileUpload.objects.filter(id=pk)).values()
        if len(Chaptervideos) == 0:
            return Response({'Chaptervideos': "Please Purchase First This courses"})
        else:
            Chaptervideos = FileUpload.objects.filter(id=pk).values('id', 'image', 'name', 'url')
            watchcount = Count.objects.filter(mediafile__in=Chaptervideos.values('id'), user_id=userv).values('mediafile', 'watch')
            if len(watchcount) == 0:
                watchcount = [{
                    "mediafile" : 0,
                    "watch"   :  0
                }]
            current_video = CurrentVideo.objects.filter(user_id=userv,currenv__in=Chaptervideos.values('id')).values('currenv', 'time')
            if len(current_video) == 0:
                current_video = [{
                        "currenv" : 0,
                        "time"   :  0
                    }]
            return Response({'Chaptervideos': Chaptervideos, 'current_video' : current_video, "watchcount": watchcount})
    else:
        return Response({'status': "please login First"})

from django.utils.decorators import method_decorator

class FileUploadss(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FileUploadss, self).dispatch(request, *args, **kwargs)


    
    def perform_create(self, serializer):
        data = User.objects.filter(is_staff=True).first()
        serializer.save(owner_id=data.id, name=self.request.data.get('name'), courses_id=self.request.data.get('courses'),chapter_id=self.request.data.get('chapter'), image=self.request.data.get('image'), uploadfile=self.request.data.get('uploadfile'))
        data = FileUpload.objects.order_by('-pk')[0]
        file = FileUpload.objects.get(id=data.id)
        data = str(file.uploadfile)
        sta = data.find('/')
        las = data.find('.')
        foldername = data[sta + 1:las]
        os.system("mkdir" + "  " + "../media_root/video/" + foldername)
        os.system("./bento4/bin/mp4fragment" + "  " + "../media_root/" + data + "  " + "../media_root/video/" + foldername + "/" + "fragement" + foldername + ".mp4")
        os.system("./bento4/bin/mp4dash -o" + "   " + "../media_root/video/" + foldername + "/" + "segments" + "  " + "../media_root/video/" + foldername + "/" + "fragement" + foldername + ".mp4")
        url = "/video/" + foldername + "/" + "segments" + "/stream.mpd"
        file.url = url
        file.save()
        


@api_view(["GET"])
def allcourse(request):
    data = Course.objects.all().values('id', 'title','image')
    return Response({'data' : data})


@csrf_exempt
@api_view(["GET"])
def coursechapter(request,pk):
    data = Chapter.objects.filter(course_id=pk).values('id', 'title')
    return Response({'data' : data})


from django.shortcuts import render 
def mediauploading(request): 
    return render(request, "course/home.html") 


def purcahaseget(request): 
    return render(request, "course/purcase.html") 


@csrf_exempt 
@api_view(["POST"])
def PurchaseCreate(request):
    courseid = request.data['courseid']
    chapterid = request.data['chapterid']
    mediaid = request.data['mediaid']
    userid=request.data['userid']
    userids = User.objects.get(id=userid)
    chid = Chapter.objects.get(id = chapterid)
    data = mediaid.split(',')
    pc = Purchase.objects.create(purchaseuser_id = userids.id, cours_id=courseid, chapter_id = chid.id)
    for i in data:
        for fc in FileUpload.objects.filter(id = int(i)).values('id'):
            pc.media.add(int(fc['id']))
            pc.save()
    return Response({'status': 'ok'},status=200)


# Particular Chapter all Videos
@csrf_exempt
@api_view(["GET"])
def Chaptervideo(request,pk): # Pk Course id
    Chaptervideos = FileUpload.objects.filter(chapter_id=pk ).values('id','name')
    return Response({'Chaptervideos': Chaptervideos}) 


@csrf_exempt
@api_view(["GET"])
def allmock(request):
    data = NumberofMock.objects.all().values('id', 'name')
    return Response({'data': data})



@csrf_exempt
@api_view(["GET", "POST"])
def MockAnswerList(request):
    t = request.META['HTTP_AUTHORIZATION']
    userid = Tokens(tok=t)
    upk = userid.user.id
    courseid = request.data['courseid']
    mock = request.data['mock']
    datalen = MockTestProgress.objects.filter(student_id=upk, cours_id=int(courseid), mock_id=int(mock))
    if len(datalen) != 0:
        num = NumberOfQuestions.objects.get(id=1)
        totalquestions = int(num.mock)
        totalcorrect = MockTestProgress.objects.filter(student_id=upk, is_right=True, cours_id=int(courseid), mock_id=int(mock)).count()
        percentage = int((totalcorrect / totalquestions) * 100)
        return Response({"msg": "You Got Percentage Is", "percentage": percentage}, status=202)
    else:
        num = NumberOfQuestions.objects.get(id=1)
        qdata = MockTest.objects.filter(cours_id=int(courseid), mock_id=int(mock)).values('id', "question",'text1', 'text2','text3').order_by('?')[0:int(num.mock)]
        return Response({"msg": "progress", "qdata": qdata}, status=200)


@csrf_exempt
@api_view(["POST"])
def MockSubmitAnswer(request,pk,cpk):
    t = request.META['HTTP_AUTHORIZATION']
    userid=Tokens(tok=t)
    upk=userid.user.id
    for i in request.data:
        try:
            data=MockTest.objects.get(cours_id=pk, mock_id=cpk, id=request.data[i]['id'],is_correct=request.data[i]['answer'])
            MockTestProgress.objects.create(student_id=upk,cours_id=pk, mock_id=cpk,  question_id=request.data[i]['id'],is_right=True)
        except ObjectDoesNotExist:
            MockTestProgress.objects.create(student_id=upk,cours_id=pk, mock_id=cpk, question_id=request.data[i]['id'],is_right=False)
    return Response({"status": "Thanks For Submitting the answer"})


@csrf_exempt
@api_view(["POST"])
def MockScore(request, pk):
    courseid = request.data['courseid']
    mock = request.data['mock']
    num = NumberOfQuestions.objects.get(id=1)
    totalquestions = int(num.mock)
    totalcorrect = MockTestProgress.objects.filter(student_id=pk, is_right=True, cours_id=int(courseid),mock_id=int(mock)).count()
    percentage = int((totalcorrect / totalquestions) * 100)
    try:
        MockTestPercentage.objects.get(student_id=pk, cours_id=int(courseid),mock_id=int(mock))
    except ObjectDoesNotExist:
        MockTestPercentage.objects.create(student_id=pk, cours_id=int(courseid),mock_id=int(mock), percentag=percentage)
    return Response({"status": "You Got Percentage Is", "percentage": percentage})


@csrf_exempt
@api_view(["GET"])
def mockpercentage(request):
    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid = Token.objects.get(key=t)
        user = int(userid.user.id)
        if userid.user.id is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # data = Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'),status=True).values()
            allweight = 0
            allcourse = 0
            for i in Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'),status=True).values():
                cid = int(i['id'])
                allcourse += 1
                for j in MockTestPercentage.objects.filter(cours_id = cid, student_id=user).values():
                    data = int(j['percentag'])
                    allweight += data
            return Response({"allweight": allweight, "allcourse" : allcourse})
    except ObjectDoesNotExist:
        return Response({"Fail": "Session Logout"})


@csrf_exempt
@api_view(["GET", "POST"])
def AssignmentsList(request):
    courseid = request.data['courseid']
    chapterid = request.data['chapterid']
    num = NumberOfQuestions.objects.get(id=1)
    t = request.META['HTTP_AUTHORIZATION']
    userid = Tokens(tok=t)
    upk = userid.user.id
    datalen = AssignmentsProgress.objects.filter(student_id=upk, cours_id=int(courseid), chapter_id=int(chapterid))
    if len(datalen) != 0:
        totalquestions = int(num.assement)
        totalcorrect = AssignmentsProgress.objects.filter(student_id=upk, cours_id=int(courseid), chapter_id=int(chapterid), is_right=True).count()
        percentage = int((totalcorrect / totalquestions) * 100)
        return Response({"msg": "You Got Percentage Is", "percentage": percentage}, status=202)
    else:
        qdata = AssignmentsTest.objects.filter(cours_id=int(courseid), chapter_id=int(chapterid)).values('id', "question", 'text1', 'text2','text3').order_by('?')[0:int(num.assement)]
        return Response({"msg": "progress", "qdata": qdata}, status=200)


@csrf_exempt
@api_view(["POST"])
def AssignmentsSubmitAnswer(request, cpk, pk):
    t = request.META['HTTP_AUTHORIZATION']
    userid = Tokens(tok=t)
    pk = userid.user.id
    for i in request.data:
        try:
            data = AssignmentsTest.objects.get(cours_id=cpk, chapter_id=pk, id=request.data[i]['id'],is_correct=request.data[i]['answer'])
            AssignmentsProgress.objects.create(cours_id=cpk, chapter_id=pk, student_id=pk, question_id=request.data[i]['id'],is_right=True)
        except ObjectDoesNotExist:
            AssignmentsProgress.objects.create(cours_id=cpk, chapter_id=pk, student_id=pk, question_id=request.data[i]['id'],is_right=False)
    return Response({"status": "Thanks For Submitting the answer"})


@csrf_exempt
@api_view(["POST"])
def AssignmentsScore(request, pk):
    courseid = request.data['courseid']
    chapterid = request.data['chapterid']
    num = NumberOfQuestions.objects.get(id=1)
    totalquestions = int(num.mock)
    totalcorrect = AssignmentsProgress.objects.filter(student_id=pk, chapter_id=int(chapterid), cours_id=int(courseid), is_right=True).count()
    percentage = int((totalcorrect / totalquestions) * 100)
    try:
        AssignmentsPercentage.objects.get(student_id=pk, chapter_id=int(chapterid), cours_id=int(courseid))
    except ObjectDoesNotExist:
        AssignmentsPercentage.objects.create(student_id=pk, chapter_id=int(chapterid), cours_id=int(courseid), percentag=percentage)
    return Response({"status": "You Got Percentage Is", "percentage": percentage})


@csrf_exempt
@api_view(["GET"])
def assegmentpercentage(request):
    t = request.META['HTTP_AUTHORIZATION']
    try:
        userid = Token.objects.get(key=t)
        user = int(userid.user.id)
        if userid.user.id is None:
            return Response({"Fail": "User Not Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            allcourse =  Course.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('cours'),status=True).count()
            allchapter =  Chapter.objects.filter(id__in=Purchase.objects.filter(purchaseuser=userid.user).values('chapter')).count()
            allweight =  AssignmentsPercentage.objects.filter(student_id=user).values('percentag')
            return Response({"allweight": allweight, "allchapter":allchapter, "allcourse": allcourse})
    except ObjectDoesNotExist:
        return Response({"Fail": "Session Logout"})


