from django.shortcuts import render, redirect, get_object_or_404
from .models import Child, Book, ReadingRecord
from .forms import ChildForm, BookForm, ReadingRecordForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils.timezone import localdate
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    today = localdate()
    today_records = ReadingRecord.objects.filter(
        date=today,
        family_id = request.user.family_id  #家族ごと見えるように
    ).order_by('-created_at')
    
    return render(request,'picture_book_app/home.html', context={
        'today_records': today_records,
        'today': today,
    })
    

# 子ども一覧画面
@login_required
def child_list(request):
    children = Child.objects.filter(family_id=request.user.family_id)
    return render(request, 'picture_book_app/child_list.html', context={
        'children':children,
    })
    
# 子ども登録画面
@login_required
def child_create(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)  #一旦保存止める
            child.family_id = request.user.family_id  #家族IDセット
            child.save()
            return redirect ('picture_book_app:child_list')
        
    else:
        form = ChildForm()
    return render(request, 'picture_book_app/child_registration.html', context={
        'form': form,
    })


# 子ども編集
@login_required
def child_update(request, pk):
    child = get_object_or_404(Child, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect('picture_book_app:child_list')
    
    else:
        form = ChildForm(instance=child)
    return render(request, 'picture_book_app/child_update.html', context={
        'form': form,
        'child': child,
    })


# 子ども削除
@login_required
def child_delete(request, pk):
    child = get_object_or_404(Child, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        child.delete()
        return redirect('picture_book_app:child_list')
    
    return render(request, 'picture_book_app/child_update.html', context={
        'child': child,
    })


# 絵本新規登録画面
@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.family_id = request.user.family_id
            book.save()
            return redirect('picture_book_app:book_list')
    else:
        form = BookForm()
    
    return render(request, 'picture_book_app/book_create.html', {
        'form': form,
    })


# 絵本一覧画面
@login_required
def book_list(request):
    query = request.GET.get('q')
    author = request.GET.get('author')
    publisher = request.GET.get('publisher')
    
    # 家族ごと見れるように
    books = Book.objects.filter(family_id = request.user.family_id)
    
    # 検索機能
    if query:
        books = books.filter(
            Q(title__icontains=query)|
            Q(author__icontains=query)|
            Q(publisher__icontains=query)
        )
    elif author:
        books = books.objects.filter(author=author)
        
    elif publisher:
        books = books.objects.filter(publisher=publisher)
    
        
    # ページネーション
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'picture_book_app/book_list.html', context={
        'books': page_obj,
        'query': query,
        'author': author,
        'publisher': publisher,
    })


# 絵本編集
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('picture_book_app:book_list')
            
    else:
        
        form = BookForm(instance=book)
    return render(request, 'picture_book_app/book_update.html', context={
        'form': form,
        'book': book,
    })

# 絵本削除
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('picture_book_app:book_list')


# 絵本詳細画面
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, family_id=request.user.family_id)
    return render(request, 'picture_book_app/book_detail.html', context={
        'book': book,
    })
    

# 絵本の読み聞かせ記録登録画面
@login_required
def reading_record_create(request):
    if request.method == 'POST':
        form = ReadingRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.family_id = request.user.family_id
            record.save()
            form.save_m2m()
            return redirect('picture_book_app:reading_record_list')
    
    else:
        form = ReadingRecordForm()
        
    return render(request, 'picture_book_app/reading_record_create.html', context={
        'form': form,
    })
    
# 絵本の読み聞かせ記録一覧画面
@login_required
def reading_record_list(request):
    child_id = request.GET.get('child')  #子どもの絞り込み
    query = request.GET.get('q')  #絵本のフリーワード検索
    
    records = ReadingRecord.objects.filter(family_id=request.user.family_id)
    
    if child_id:
        records = records.filter(child__id=child_id)
    if query:
        records = records.filter(book__title__icontains=query)
    
    records = records.order_by('-date')
    
    # ページネーション
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'picture_book_app/reading_record_list.html', context={
        'records': page_obj,
        'children': Child.objects.filter(family_id=request.user.family_id),
        'query': query,
        'select_child': child_id
    })
    

# 読み聞かせ記録の詳細画面
@login_required
def reading_record_detail(request, pk):
    record = get_object_or_404(ReadingRecord, pk=pk, family_id=request.user.family_id)
    return render(request, 'picture_book_app/reading_record_detail.html', context={
        'record': record,
    })
    

# 読み聞かせ記録編集画面
@login_required
def reading_record_update(request,pk):
    record = get_object_or_404(ReadingRecord, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        form = ReadingRecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('picture_book_app:reading_record_detail', pk=record.pk)
        
    else:
        form = ReadingRecordForm(instance=record)
    return render(request, 'picture_book_app/reading_record_update.html', context={
        'form': form,
        'record': record,
    })

# 読み聞かせ記録削除画面
@login_required
def reading_record_delete(request,pk):
    record = get_object_or_404(ReadingRecord, pk=pk, family_id=request.user.family_id)
    
    if request.method == 'POST':
        record.delete()
        return redirect('picture_book_app:reading_record_list')


# 好きな絵本ランキング
@login_required
def book_ranking(request):
    child_id = request.GET.get('child_id')
    
    records = ReadingRecord.objects.filter(family_id=request.user.family_id)
    
    if child_id:
        records = records.filter(child_id=child_id)

    # 絵本ごと読んだ回数を集計
    ranking = (
        records.values('book__id', 'book__title')
        .annotate(total_reads=Sum('read_count'))
        .order_by('-total_reads')
    )
    
    # ページネーション
    paginator = Paginator(ranking, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    # 順位の計算
    start_rank = (page_obj.number - 1) * paginator.per_page + 1
    ranked_books = []
    
    for r in page_obj.object_list:
        ranked_books.append({'rank': start_rank, 'book_title': r['book__title'], 'total_reads': r['total_reads']})
        start_rank += 1
    
    total_reads = records.aggregate(total=Sum('read_count'))['total'] or 0
    
    return render(request, 'picture_book_app/book_ranking.html', context={
        'books_with_rank': ranked_books,
        'children': Child.objects.filter(family_id=request.user.family_id),
        'selected_child_id': child_id,
        'total_reads': total_reads,
        'page_obj': page_obj,
    })