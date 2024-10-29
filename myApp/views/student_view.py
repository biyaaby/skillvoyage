from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from ..models import *
from ..forms import *
from ..models import Feedback  # Assuming you have a Feedback model
from django.contrib import messages
from django.contrib.messages import success

def find_art(request):
    return render(request, 'find_art.html')

def submit_feedback(request, lesson_id):
    if request.method == 'POST':
        rating = request.POST['rating']
        feedback_text = request.POST['feedback']
        user = request.user
        lesson = CourseLesson.objects.get(id=lesson_id)

        # Save the feedback to the database
        Feedback.objects.create(user=user, lesson=lesson, rating=rating, feedback=feedback_text)

        # Use messages to show a success message
        messages.success(request, 'Thank you for your feedback!')
        return redirect('student_view_lesson', id=lesson_id)

    
@login_required
def student_home(request):
    context = {}
    context['courses'] = EnrolledCourse.objects.prefetch_related('course__lessons').filter(student=request.user)
    return render(request, 'student_home.html', context)

def student_more_courses(request):
    context = {}
    enrolled_course_ids = list(EnrolledCourse.objects.filter(student=request.user).values_list('course_id', flat=True))
    context['courses'] = Course.objects.filter(status='published').exclude(id__in=enrolled_course_ids)
    print(context['courses'])
    return render(request, 'student_more_courses.html', context)


def student_enroll(request, id):
    course = get_object_or_404(Course, id=id)
    # Check if the user has already enrolled in the course.
    if EnrolledCourse.objects.filter(course=course, student=request.user).exists():
        return redirect(reverse('student_home'))
    
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'course': course
    }
    
    if request.method == 'GET':
        return render(request, 'student_enroll.html', context)
    # EnrolledCourse.objects.create(course=course, student=request.user)
    return redirect(reverse('student_home'))

def student_enroll_success(request, id):
    course = get_object_or_404(Course, id=id)
    # Check if the user has already enrolled in the course.
    if EnrolledCourse.objects.filter(course=course, student=request.user).exists():
        return redirect(reverse('student_home'))
    
    EnrolledCourse.objects.create(course=course, student=request.user)
    return redirect(reverse('student_home'))

def student_enroll_failure(request):
    return redirect(reverse('student_home'))

@csrf_exempt
def student_create_course_payment(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        try:
            # Create a new Checkout Session for the payment
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Payment methods allowed
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': course.name,
                        },
                        'unit_amount': int(course.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://127.0.0.1:8000/student/enroll/success/{course.id}',  # Redirect after success
                cancel_url='http://127.0.0.1:8000/student/enroll/failre/',     # Redirect if canceled
            )
            # Redirect the user to the Stripe Checkout page
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

def student_take_lesson(request, id):
    lesson = get_object_or_404(CourseLesson, id=id)
    course = Course.objects.filter(id=lesson.course_id)
    lessons = CourseLesson.objects.filter(course_id=lesson.course_id)
    context = {
        'course': course,
        'lesson': lesson,
        'lessons': lessons
    }
    return render(request, 'student_view_lesson.html', context)

def student_store(request):
    products = Product.objects.filter(status='active')
    return render(request, 'student_store.html', {'products': products})

def student_cart_add(request, id):
    product = get_object_or_404(Product, id=id)
    # Add to cart if the product is not added yet
    if Cart.objects.filter(product=product, user=request.user).exists():
        cart = Cart.objects.get(product=product, user=request.user)
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(product=product, user=request.user, quantity=1)
    return redirect(reverse('student_cart'))

def student_cart_delete(request, id):
    cart = get_object_or_404(Cart, id=id)
    cart.delete()
    return redirect(reverse('student_cart'))

def student_cart(request):
    context = {}
    context['carts'] = Cart.objects.filter(user=request.user)
    return render(request, 'student_cart.html', context)

def student_place_order(request):
    context = {}
    if request.method == 'GET':
        context['form'] = OrderForm()
        return render(request, 'student_place_order.html', context)

    elif request.method == 'POST':
        form = OrderForm(data=request.POST)
        context['form'] = form
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            # Calculating total price
            total = 0
            for cart in Cart.objects.filter(user=request.user):
                total += cart.quantity * cart.product.price

            order.price = total
            order.save()
            for cart in Cart.objects.filter(user=request.user):
                OrderItem.objects.create(
                    order=order,
                    product=cart.product,
                    quantity=cart.quantity
                )
            # Redirect to payment page and pass order id
            return redirect(reverse('student_order_payment', args=[order.id]))
        return render(request, 'student_place_order.html', context)

def student_order_payment(request, id):
    context = {}
    context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
    context['order'] = get_object_or_404(Order, id=id)
    return render(request, 'student_order_payment.html', context)

def student_order_success(request, id):
    order = get_object_or_404(Order, id=id)
    order.success = True
    # clear cart items
    Cart.objects.filter(user=request.user).delete()
    order.save()
    return redirect(reverse('student_orders'))

def student_orders(request):
    context = {}
    context['orders'] = Order.objects.filter(user=request.user, success=True)
    return render(request, 'student_orders.html', context)

@csrf_exempt
def student_create_order_payment(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = get_object_or_404(Order, id=id)
    order_items = OrderItem.objects.filter(order=order)
    if request.method == 'POST':
        try:
            # Create a new Checkout Session for the payment
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Payment methods allowed
                # Create order items based on order

                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Store Order',
                        },
                        'unit_amount': int(order.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://127.0.0.1:8000/student/orders/success/{order.id}',  # Redirect after success
                cancel_url='http://127.0.0.1:8000/student/cart/',     # Redirect if canceled
            )
            # Redirect the user to the Stripe Checkout page
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)