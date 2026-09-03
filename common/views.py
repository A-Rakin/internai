from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'landing/home.html'

class AboutView(TemplateView):
    template_name = 'landing/about.html'

class FeaturesView(TemplateView):
    template_name = 'landing/features.html'

class HowItWorksView(TemplateView):
    template_name = 'landing/how_it_works.html'

class PricingView(TemplateView):
    template_name = 'landing/pricing.html'

class FaqView(TemplateView):
    template_name = 'landing/faq.html'

class ContactView(TemplateView):
    template_name = 'landing/contact.html'

class PrivacyView(TemplateView):
    template_name = 'landing/privacy.html'

class RulesView(TemplateView):
    template_name = 'landing/rules.html'
