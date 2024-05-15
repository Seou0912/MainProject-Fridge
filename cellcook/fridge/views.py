from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Ingredient, Menu, IngredientMenuMapping, Recipe
import openai
import os
from django.conf import settings


@login_required
def fridge_main(request):
    """
    냉장고 재료 리스트를 보여주는 뷰
    """
    ingredients = Ingredient.objects.all()
    return render(request, "fridge-main.html", {"ingredients": ingredients})


@login_required
def ingredient_create(request):
    if request.method == "POST":
        ingredient_name = request.POST.get("ingredient_name")
        ingredient_type = request.POST.get("ingredient_type")
        expiration_date = request.POST.get("expiration_date")

        ingredient = Ingredient.objects.create(
            user=request.user,
            ingredient_name=ingredient_name,
            ingredient_type=ingredient_type,
            expiration_date=expiration_date,
        )

        return redirect("fridge-main")
    return render(request, "ingredient.html")


@login_required
def get_user_ingredients(user):
    openai.api_key = settings.OPENAI_API_KEY
    """
    주어진 사용자의 모든 재료 이름을 리스트로 반환합니다.
    """
    ingredients = Ingredient.objects.filter(user=user)
    ingredient_names = [ingredient.ingredient_name for ingredient in ingredients]
    return ingredient_names


def get_menu_recommendations(ingredients):
    """
    주어진 재료 목록을 기반으로 OpenAI GPT-4 Turbo를 사용하여 레시피 추천을 생성합니다.
    """
    try:
        ingredients_text = ", ".join(ingredients)
        prompt = f"Given the ingredients {ingredients_text}, suggest a recipe that uses these ingredients."
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # 로그를 남기거나 적절한 에러 처리를 수행
        return "An error occurred while generating recommendations."


def recommend_menu(request):
    if request.method == "POST":
        # 사용자가 제출한 재료 목록을 받아옵니다.
        ingredients = request.POST.getlist("ingredients")

        # menu 추천을 받아옵니다.
        recommended_menu = get_menu_recommendations(ingredients)

        # 추천된 menu를 menu.html에 전달합니다.
        return render(request, "menu.html", {"recommended_menu": recommended_menu})
    else:
        # GET 요청 시, 재료 입력 폼을 보여주는 페이지를 렌더링합니다.
        return render(request, "ingredients.html")


@login_required
def ingredient_menu_mapping_create(request):
    if request.method == "POST":
        ingredient_id = request.POST.get("ingredient_id")
        menu_id = request.POST.get("menu_id")

        mapping = IngredientMenuMapping(ingredient_id=ingredient_id, menu_id=menu_id)
        mapping.save()
        return redirect("ingredient_menu_mapping_list")
    return render(request, "ingredient_menu_mapping.html")


@login_required
def get_recipe_details(request):
    if request.method == "POST":
        selected_menu = request.POST.get("selected_menu")

        try:
            prompt = f"How to cook {selected_menu}?"
            response = openai.Completion.create(
                model="gpt-4-turbo",
                prompt=prompt,
                max_tokens=800,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            recipe_details = response.choices[0].text.strip()
            return render(request, "recipe.html", {"recipe_details": recipe_details})
        except Exception as e:
            return render(request, "recipe.html", {"error": str(e)})
    else:
        return redirect("menu")

        # 메뉴 선택 페이지로 리디렉션
