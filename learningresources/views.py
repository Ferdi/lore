"""
Views for learningresources app.
"""

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403

from learningresources.api import get_repos
from learningresources.forms import RepositoryForm
from learningresources.models import Repository
from role.api import assign_user_to_repo_group
from role.permissions import GroupTypes


@login_required
def welcome(request):
    """
    Greet the user, show available repositories.
    """
    return render(
        request,
        "welcome.html",
        {"repos": get_repos(request.user)}
    )


@login_required
@permission_required_or_403(
    '{}.add_{}'.format(
       Repository._meta.app_label,  # pylint: disable=protected-access
       Repository._meta.model_name  # pylint: disable=protected-access
    )
)
def create_repo(request):
    """
    Create a new repository.
    """
    form = RepositoryForm()
    if request.method == "POST":
        form = RepositoryForm(data=request.POST)
        if form.is_valid():
            repo = form.save(request.user)
            assign_user_to_repo_group(request.user, repo, GroupTypes.repo_administrator)
            return redirect(reverse("welcome"))
    return render(
        request,
        "create_repo.html",
        {"form": form},
    )
