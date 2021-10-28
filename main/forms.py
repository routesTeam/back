from django import forms

class CitiesForm(forms.Form):
  first_city  = forms.CharField(label='Введите пункт отправления:', 
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'})
              )
  second_city = forms.CharField(label='Введите пункт назначения:', 
                  widget=forms.TextInput(attrs=
                    {'class': 'form-control', 'placeholder': 'Санкт-Петербург'}
                ))