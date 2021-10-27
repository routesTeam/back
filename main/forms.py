from django import forms


class CitiesForm(forms.Form):
  firstCity  = forms.CharField(label='Введите пункт отправления:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'}))
  secondCity = forms.CharField(label='Введите пункт назначения:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Санкт-Петербург'}))