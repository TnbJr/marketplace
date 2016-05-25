# from itertools import chain
# from operator import attrgetter
# from django.utils import timezone
# from posts.models import ContentPost
# from reviews.models import ProductReview
# from videos.models import Video 

# def query_chain(*args, **kwargs):
# 	post_queryset = ContentPost.objects.filter(draft=False, published__lte=timezone.now())
# 	review_queryset = ProductReview.objects.filter(draft=False, published__lte=timezone.now())
# 	video_queryset = Video.objects.filter(draft=False, published__lte=timezone.now())
# 	result_query = sorted(
# 		chain(post_queryset, review_queryset, video_queryset),
# 		key=attrgetter('published'), reverse=True)
# 	return result_query