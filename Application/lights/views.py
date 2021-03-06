from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Question
import OSC, time

# View showing all choices, uses generic list view
class IndexView(generic.ListView):
	template_name = 'lights/index.html'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')


#### I want a class here to handle forms
def stepThrough(request):
	return render(request,'lights/setup.html')




# function to send question ID to Processing via OSC
def sendVals(request,question_id):
	p = get_object_or_404(Question, pk=question_id)
	########## OSC section
	send_address = "127.0.0.1",5001 
	c = OSC.OSCClient() 
	c.connect(send_address) 
	msg = OSC.OSCMessage()
	msgint = int(question_id)
	msg.setAddress("/print")
	# appending ID as first item in message - important for Processing sketch
	msg.append(msgint) 
		### question_id mapping for now
		# 1: Fourth
		# 2: Third 
		# 3: ** ON
		# 4: ** OFF
		# 5: Second 
		# 6: First 
		# 7: Fifth 
		# 8: ** North 
		# 9: ** ON, Half
		# 10: ** ON, Dim
	roomDict = {
		6:[i for i in range(40)],
		5:[i for i in range(40,80)],
		2:[i for i in range(80,120)],
		1:[i for i in range(120,160)],
		7:[i for i in range(160,200)],
		8:[i for i in range(3,8)+range(43,48)+range(83,88)+range(123,128)+range(163,168)]
	}
	
	if msgint in roomDict:
		msg.append(roomDict[msgint])
	else:
		pass #something better here

	c.send(msg)
	## Redirect to stay on main page
	return HttpResponseRedirect(reverse('lights:index',))


def dbTest(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	send_address = "127.0.0.1",5001 
	c = OSC.OSCClient() 
	c.connect(send_address) 
	msg = OSC.OSCMessage()
	msgint = int(question_id)
	msg.setAddress("/print")
	msg.append(2)
	temp = Question.objects.filter(question_text__startswith="All")
	testList = [t.id for t in temp]
	msg.append(testList)
	c.send(msg)

	return HttpResponseRedirect(reverse('lights:detail', args=(p.id,)))

	