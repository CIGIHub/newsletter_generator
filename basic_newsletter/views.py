from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from basic_newsletter.models import Issue, NewsItem, Newsletter
from basic_newsletter.forms import IssueForm, NewsItemForm, \
    HeadlineNewsItemForm, CreateIssueForm, EmailTestForm


# Display the list of issues on the homepage.
# Also display a form to create a new issue for a pre-existing newsletter type
@login_required
def home(request, template='basic_newsletter/home.html'):
    newsletter_list = Newsletter.objects.all()

    newsletter_issue_list = []
    for newsletter in newsletter_list:
        newsletter_issue_list.append((newsletter,
                                      Issue.objects
                                      .filter(published_state='Draft',
                                              newsletter=newsletter)
                                      .order_by('-issue_date'),
                                      Issue.objects
                                      .filter(published_state='Ready to Test',
                                              newsletter=newsletter)
                                      .order_by('-issue_date'),
                                      Issue.objects
                                      .filter(published_state='Published',
                                              newsletter=newsletter)
                                      .order_by('-issue_date'),
        ))

    context = dict(newsletter_issue_list=newsletter_issue_list, )

    return render(request, template, context)


# Create a new issue of a newsletter as selected from the homepage
@login_required
def create_issue(request, template='basic_newsletter/issue_create.html'):
    if request.method == 'POST':
        form = CreateIssueForm(request.POST)
        if form.is_valid():
            issue = Issue()
            newsletter = Newsletter.objects.get(
                id=request.POST['newsletter_type'])
            issue.newsletter = newsletter
            issue_date = datetime(year=int(request.POST['issue_date_year']),
                                  month=int(request.POST['issue_date_month']),
                                  day=1)
            issue.issue_date = issue_date
            issue.published_state = 'Draft'
            issue.save()


            issue.story_categories = request.POST.getlist('sections')
            issue.save()
            return redirect('newsletter:edit_issue', issue_id=issue.id)
    else:
        form = CreateIssueForm()

    context = dict(
        form=form,
    )

    return render(request, template, context)


@login_required
def edit_issue(request, issue_id, template='basic_newsletter/issue_edit.html'):
    issue = Issue.objects.get(id=issue_id)
    headline_formsets = []
    non_headline_formsets = []

    if request.method == 'POST':

        errors = False
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.template = issue.newsletter.template
            issue.save()

        for headline_category in issue.headline_categories:
            headline_news_item_form_set = modelformset_factory(NewsItem,
                                                           form=HeadlineNewsItemForm,
                                                           can_delete=True)

            form_headline = headline_news_item_form_set(request.POST, request.FILES,
                                                    prefix=headline_category.code_name)
            headline_formsets.append((headline_category, form_headline))

            if form_headline.is_valid():
                new_headlines = form_headline.save(commit=False)
                for new_headline in new_headlines:

                    new_headline.feature_type = headline_category
                    new_headline.issue = issue
                    new_headline.save()

                for deleted_headlines in form_headline.deleted_objects:
                    deleted_headlines.delete()
            else:
                errors = True

        for category in issue.non_headline_categories:
            news_item_form_set = modelformset_factory(NewsItem,
                                                           form=NewsItemForm,
                                                           can_delete=True)

            form = news_item_form_set(request.POST, request.FILES,
                                                    prefix=category.code_name)
            non_headline_formsets.append((category, form))

            if form.is_valid():
                new_stories = form.save(commit=False)
                for story in new_stories:
                    story.feature_type = category
                    story.issue = issue
                    story.save()

                for deleted_story in form.deleted_objects:
                    deleted_story.delete()
            else:
                errors = True

        if not errors:
            if request.POST.get('draft'):
                issue.published_state = 'Draft'
                issue.save()
                return redirect('newsletter:home')

            elif request.POST.get('preview'):
                return redirect('newsletter:preview_issue', issue_id=issue.id)

            elif request.POST.get('save_published'):
                issue.published_state = 'Published'
                issue.save()
                return redirect('newsletter:home')

    else:

        for headline_category in issue.headline_categories:

            feature_queryset = NewsItem.objects.filter(issue=issue,
                                                   feature_type=headline_category)

            extra_forms = 1
            if len(feature_queryset) > 0:
                extra_forms = 0

            headline_news_item_form_set = modelformset_factory(NewsItem,
                                                           form=HeadlineNewsItemForm,
                                                           can_delete=True,
                                                           extra=extra_forms)


            form_headline = headline_news_item_form_set(queryset=feature_queryset,
                                                      prefix=headline_category.code_name)

            headline_formsets.append((headline_category, form_headline))

        for category in issue.non_headline_categories:

            feature_queryset = NewsItem.objects.filter(issue=issue,
                                                       feature_type=category)
            extra_forms = 1
            if len(feature_queryset) > 0:
                extra_forms = 0
            news_item_form_set = modelformset_factory(NewsItem,
                                                      form=NewsItemForm,
                                                      can_delete=True,
                                                      extra=extra_forms)


            form = news_item_form_set(queryset=feature_queryset,
                                      prefix=category.code_name)

            non_headline_formsets.append((category, form))

    context = dict(
        issue=issue,
        headline_formsets=headline_formsets,
        non_headline_formsets=non_headline_formsets,
    )

    return render(request, template, context)


# Display the preview of an issue in the corresponding template.
@login_required
def preview_issue(request, issue_id, template='basic_newsletter/preview_issue.html'):
    issue = Issue.objects.get(id=issue_id)

    if request.method == 'POST':

        if request.POST.get('to_test'):
            errors = issue.is_complete()
            for error in errors:
                messages.error(request, error)

            if len(errors) == 0:
                issue.mark_ready_to_publish(request)
                return redirect('newsletter:home')
        elif request.POST.get('send_email'):
            return redirect('newsletter:test_issue', issue_id=issue.id)
            pass
        elif request.POST.get('draft'):
            issue.published_state = 'Draft'
            issue.save()
            return redirect('newsletter:edit_issue', issue_id=issue.id)
        elif request.POST.get('close'):
            return redirect('newsletter:home')

    context = dict(
        issue=issue,
    )

    return render(request, template, context)


@login_required
def preview_issue_html(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    template = issue.html_email_template

    context = dict(
        issue=issue,
        tracking=False,
    )

    return render(request, template, context)


@login_required
def preview_issue_text(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    template = issue.plain_text_email_template

    context = dict(
        issue=issue,
    )

    return render(request, template, context)


@login_required
def delete_issue(request, issue_id, template='basic_newsletter/delete_issue.html'):
    issue = Issue.objects.get(id=issue_id)

    if request.POST.get('delete'):
        issue.delete()
        return redirect('newsletter:home')

    elif request.POST.get('cancel_delete'):
        return redirect('newsletter:home')

    else:

        context = dict(
            issue=issue,
        )

        return render(request, template, context)


@login_required
def test_issue(request, issue_id, template='basic_newsletter/test_email.html'):
    issue = Issue.objects.get(id=issue_id)
    if request.method == 'POST':
        form = EmailTestForm(request.POST)

        if request.POST.get('send'):
            recipient = form["recipient"].value()
            sender = form["sender"].value()

            issue.send_test(recipient, sender)
            messages.success(request,
                             "Test email sent to %s for %s." % (recipient,
                                                                issue))

        return redirect('newsletter:home')
    else:
        form = EmailTestForm()

    context = dict(
        form=form,
        issue=issue,
    )
    return render(request, template, context)


@login_required
def publish_issue(request, issue_id, template="basic_newsletter/publish_issue.html"):
    issue = Issue.objects.get(id=issue_id)

    if request.POST.get('publish'):
        issue.published_date = datetime.now()
        issue.publish(request)

        return redirect('newsletter:home')

    elif request.POST.get('cancel'):
        return redirect('newsletter:home')
    else:
        context = dict(
            issue=issue,
        )

        return render(request, template, context)


@login_required
def reupload_issue(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    issue.reupload()

    return redirect('newsletter:home')