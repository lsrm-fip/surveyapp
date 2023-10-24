from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from .models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from .backends import EmailBackend


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        print("data: ", data)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {"email_error": "Alamat email tidak sesuai"}, status=400
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "email_error": "Alamat email sudah terdaftar. Silahkan masuk ke halaman login"
                },
                status=409,
            )
        return JsonResponse({"email_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        context = {"fieldValues": request.POST}

        if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, "Password terlalu pendek")
                return render(request, "authentication/register.html", context)

            if password != password2:
                messages.error(request, "Konfirmasi kata sandi tidak sesuai")
                return render(request, "authentication/register.html", context)

            user = User.objects.create_user(email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_body = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }

            link = reverse(
                "activate",
                kwargs={"uidb64": email_body["uid"], "token": email_body["token"]},
            )

            email_subject = "Aktivasi akun - Layanan Survey Resiliensi UNIMED"

            activate_url = "http://" + current_site.domain + link

            email = EmailMessage(
                email_subject,
                "Silahkan klik tautan berikut untuk mengaktifkan akun anda:\n\n"
                + activate_url,
                "noreply@semycolon.com",
                [email],
            )
            email.send(fail_silently=False)
            messages.success(
                request,
                "Registrasi berhasil. Silahkan cek email anda untuk aktivasi akun",
            )
            return render(request, "authentication/register.html")

        return render(request, "authentication/register.html")


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect("login" + "?message=" + "Akun sudah aktif")

            if user.is_active:
                return redirect("login")
            user.is_active = True
            user.save()

            messages.success(request, "Akun berhasil diaktifkan")
            return redirect("login")

        except Exception as ex:
            pass

        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        if email and password:
            user = EmailBackend.authenticate(
                self, request, username=email, password=password
            )
            if user:
                print(user)
                if user.is_active:
                    auth.login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    messages.success(
                        request, "Selamat datang, Anda telah berhasil masuk"
                    )
                    return redirect("homepage:index")
                messages.error(
                    request,
                    "Akun Anda belum aktif, silahkan cek kembali email Anda untuk mengaktifkan",
                )
                return render(request, "authentication/login.html")
            messages.error(request, "Data tidak valid, silahkan coba lagi")
            return render(request, "authentication/login.html")

        messages.error(request, "Mohon lengkapi kolom berikut")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "Anda telah logout")
        return redirect("login")
