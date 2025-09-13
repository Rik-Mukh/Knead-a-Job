from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        resume = self.get_object()
        # Unset all other default resumes for this user
        Resume.objects.filter(user=request.user, is_default=True).update(is_default=False)
        # Set this resume as default
        resume.is_default = True
        resume.save()
        return Response({'status': 'Resume set as default'})
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        try:
            default_resume = Resume.objects.filter(user=request.user, is_default=True).first()
            if default_resume:
                serializer = self.get_serializer(default_resume)
                return Response(serializer.data)
            else:
                return Response({'detail': 'No default resume found'}, status=status.HTTP_404_NOT_FOUND)
        except Resume.DoesNotExist:
            return Response({'detail': 'No default resume found'}, status=status.HTTP_404_NOT_FOUND)
