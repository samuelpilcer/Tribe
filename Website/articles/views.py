from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required

# Create your views here.

from articles.models import Article, Categorie

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles

    if len(articles)>10:
        n=5
    else:
        n=int(len(articles)/2)

    articles1=[]
    articles2=[]
    for i in range(n):
        articles1.append(articles[2*i])
        articles2.append(articles[2*i+1])

    if len(articles)<10 and 2*int(len(articles)/2) != len(articles):
        articles1.append(articles[len(articles)-1])
    
    return render(request, 'blog/accueil.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2})


def lire(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/lire.html', {'article': article})

@login_required
def new(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ArticleForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        new_article=Article()
        new_article.auteur=request.user
        new_article.titre = form.cleaned_data.get('titre')
        new_article.contenu = form.cleaned_data.get('contenu')
        new_article.categorie = form.cleaned_data.get('categorie')
        new_article.save()

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/new.html', locals())