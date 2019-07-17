from django import forms


class ClientForm(forms.Form):
    client = forms.CharField(
        label='Tapez votre numero de client'
    )

    def clean_client(self):
        client = self.cleaned_data['client']
        if not client.isdigit():
            raise forms.ValidationError("L'identifiant du client doit être un nombre positif")
        else:
            if int(client) <= 0:
                raise forms.ValidationError("Entrez un identifiant positif")

        return client
