from .models import ContentPost
from faker import Factory
faker = Factory.create()

def faker_post():
	count = 0
	for i in range(21):
		ContentPost.objects.create(
				title=faker.sentence(),
				content = faker.text(max_nb_chars=1000)
				)
		count += 1
faker_post()