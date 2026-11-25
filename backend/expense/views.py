from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
# Create your views here.
from django.db.models import Sum

import traceback

#Signup API
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fullname = data.get('FullName')
        email = data.get('Email')
        password = data.get('Password')
        
        if UserDeatil.objects.filter(Email=email).exists():
            return JsonResponse({'message':'Email already exists'}, status=400)
        UserDeatil.objects.create(FullName= fullname,Email=email,Password=password)
        return JsonResponse({'message':'User register Successfully'}, status= 201)
    

#Login API
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('Email')
        password = data.get('Password')
        
        try:
            user = UserDeatil.objects.get(Email=email, Password=password)
            return JsonResponse({'message':'Login successful','userId':user.id,'userName':user.FullName}, status=200)
        except:
            return JsonResponse({'message':'Invalid credentials'}, status= 400)


#Add-Expense
@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('UserId')
        expense_date = data.get('ExpenseDate')
        expense_item = data.get('ExpenseItem')
        expense_cost = data.get('ExpenseCost')
        
        
        user = UserDeatil.objects.get(id = user_id)
        try:
            Expense.objects.create(UserId=user,ExpenseDate=expense_date,ExpenseItem=expense_item,ExpenseCost=expense_cost)
            return JsonResponse({'message':'Expense addes successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message':'Something went wrong','error':str(e)}, status= 400)


@csrf_exempt
def manage_expense(request,user_id):
    if request.method == 'GET':      
        
        expenses = Expense.objects.filter(UserId=user_id)
        expense_list = list(expenses.values())
        return JsonResponse(expense_list,safe=False)



@csrf_exempt
def update_expense(request,expense_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        # user_id = data.get('UserId') 

    try:
        expense = Expense.objects.get(id=expense_id)
        expense.ExpenseDate = data.get('ExpenseDate',expense.ExpenseDate)
        expense.ExpenseCost = data.get('ExpenseCost',expense.ExpenseCost)
        expense.ExpenseItem = data.get('ExpenseItem',expense.ExpenseItem)
        expense.save()
        return JsonResponse({'message':'Expense updated successfully'})
    except:
        return JsonResponse({'message':'Expense not found'},status=404)
    


@csrf_exempt
def delete_expense(request,expense_id):
    if request.method == 'DELETE':
     try:
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return JsonResponse({'message':'Expense deleted successfully'}, status=200)
     except:
        return JsonResponse({'message':'Expense not found'},status=404)
     



@csrf_exempt
def search_expense(request,user_id):
    if request.method == 'GET':  
      try:
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')    
        
        expenses = Expense.objects.filter(UserId=user_id,ExpenseDate__range=[from_date,to_date])
        expense_list = list(expenses.values())
        agg = expenses.aggregate(Sum('ExpenseCost'))  #{'ExpenseCost__Sum':3500 like this it return}
        total = agg['ExpenseCost__sum'] or 0
        return JsonResponse({'expenses':expense_list,'total':total})
      except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
      return JsonResponse({'message': 'Invalid request'}, status=405)
    

@csrf_exempt
def change_password(request,user_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        old_password = data.get('oldPassword')
        new_password = data.get('newPassword') 
        
        try:
            user = UserDeatil.objects.get(id = user_id)
            if user.Password != old_password:
                return JsonResponse({'message':'Old password is incorrect'}, status=400)
            user.Password = new_password
            user.save()
            return JsonResponse({'message':'Password changed successfully'},status=200)
        except:
            return JsonResponse({'message':'User not found'}, status= 404)