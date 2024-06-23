#Proporciona el formulario de feedback a todas las plantillas

from .forms import FeedbackForm

def feedback_form(request):
    return {
        'feedback_form': FeedbackForm()
    }