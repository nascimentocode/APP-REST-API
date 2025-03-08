import flet as ft
import requests

API_BASE_URL = "http://localhost:8000/api"

def main(page: ft.Page):
    page.title = "Cadastro App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Criar aluno aba
    nome_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="Email")
    faixa_field = ft.TextField(label="Faixa")
    data_nascimento_field = ft.TextField(label="Data de Nascimento (YYYY-MM-DD)")
    create_result = ft.Text()
    
    def criar_aluno_click(e):
        payload = {
            "name": nome_field.value,
            "email": email_field.value,
            "belt": faixa_field.value,
            "birthdate": data_nascimento_field.value
        }
        
        response = requests.post(API_BASE_URL + '/', json=payload)
        
        if response.status_code == 200:
            aluno = response.json()
            create_result.value = f'Aluno criado: {aluno}'
        else:
            create_result.value = f'Erro: {response.text}'
        
        page.update()
    
    create_button = ft.ElevatedButton(text="Criar Aluno", on_click=criar_aluno_click)

    criar_aluno_tab = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_result,
            create_button,
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    # Listar aluno aba
    students_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Nome')),
            ft.DataColumn(ft.Text('Email')),
            ft.DataColumn(ft.Text('Faixa')),
            ft.DataColumn(ft.Text('Data de Nascimento')),
        ],
        rows=[]
    )
    
    list_result = ft.Text()
    
    def listar_aluno_click(e):
        response = requests.get(API_BASE_URL + '/students/')
        
        if response.status_code == 200:
            alunos = response.json()
            students_table.rows.clear()
            
            for aluno in alunos:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(aluno.get('name'))),
                        ft.DataCell(ft.Text(aluno.get('email'))),
                        ft.DataCell(ft.Text(aluno.get('belt'))),
                        ft.DataCell(ft.Text(aluno.get('birthdate'))),
                    ]
                )
                
                students_table.rows.append(row)
            
            list_result.value = f'{len(alunos)} alunos encontrados'
            page.update()
        else:
            list_result.value = f'Erro: {response.text}'
        
        page.update()
    
    list_button = ft.ElevatedButton(text="Listar Alunos", on_click=listar_aluno_click)
    listar_aluno_tab = ft.Column(
        [
            students_table,
            list_result,
            list_button
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    # Adicionar aulas tab
    email_aula_field = ft.TextField(label="Email do Aluno")
    qtd_field = ft.TextField(label="Quantidade de aulas", value="1")
    aula_result = ft.Text()
    
    def marcar_aula_click(e):
        payload = {
            "qtd": int(qtd_field.value),
            "student_email": email_aula_field.value
        }
        
        response = requests.post(API_BASE_URL + '/aula_realizada/', json=payload)
        
        if response.status_code == 200:
            aula_result.value = f'Sucesso: {response.json()}'
        else:
            aula_result.value = f'Erro: {response.text}'
        
        page.update()

    aula_button = ft.ElevatedButton(text="Marcar aula realizada", on_click=marcar_aula_click)
    
    aula_tab = ft.Column(
        [
            email_aula_field,
            qtd_field,
            aula_result,
            aula_button
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    # Progresso do aluno aba
    email_progress_field = ft.TextField(label="Email do aluno")
    progress_result = ft.Text()
    
    def consultar_progresso_click(e):
        email = email_progress_field.value
        response = requests.get(API_BASE_URL + '/progress_student/', params={'student_email': email})
        
        if response.status_code == 200:
            progress = response.json()
            progress_result.value = (
                f"Nome: {progress.get('name', '')}\n"
                f"Email: {progress.get('email', '')}\n"
                f"Faixa Atual: {progress.get('belt', '')}\n"
                f"Aulas Totais: {progress.get('total_class', 0)}\n"
                f"Aulas necessárias para a próxima faixa: {progress.get('classes_required_for_next_belt', 0)}"
            )
        else:
            progress_result.value = f"Erro: {response.text}"

        page.update()
    
    progress_button = ft.ElevatedButton(text="Consultar Progresso", on_click=consultar_progresso_click)
    progress_tab = ft.Column(
        [
            email_progress_field,
            progress_result,
            progress_button
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    # Atualizar aluno tab
    id_aluno_field = ft.TextField(label="ID do Aluno")
    nome_update_field = ft.TextField(label="Novo Nome")
    email_update_field = ft.TextField(label="Novo Email")
    faixa_update_field = ft.TextField(label="Nova Faixa")
    data_nascimento_update_field = ft.TextField(label="Nova Data de Nascimento (YYYY-MM-DD)")
    update_result = ft.Text()
    
    def atualizar_aluno_click(e):
        aluno_id = id_aluno_field.value
        if not aluno_id:
            update_result.value = "ID do aluno é necessário."
        else:
            payload = {
                "name": nome_update_field.value,
                "email": email_update_field.value,
                "belt": faixa_update_field.value,
                "birthdate": data_nascimento_update_field.value,
            }
            
            response = requests.put(API_BASE_URL + f'/alunos/{aluno_id}', json=payload)
            print(response.status_code)
            if response.status_code == 200:
                aluno = response.json()
                update_result.value = f"Aluno atualizado: {aluno}"
            else:
                update_result.value = f"Erro: {response.text}"
            
        page.update()
        
    update_button = ft.ElevatedButton(text="Atualizar Aluno", on_click=atualizar_aluno_click)
    atualizar_tab = ft.Column(
        [
            id_aluno_field,
            nome_update_field,
            email_update_field,
            faixa_update_field,
            data_nascimento_update_field,
            update_button,
            update_result,
        ],
        scroll=True,
    )
    
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Criar Aluno", content=criar_aluno_tab),
            ft.Tab(text="Listar Alunos", content=listar_aluno_tab),
            ft.Tab(text="Cadastrar Aulas", content=aula_tab),
            ft.Tab(text="Progresso do Aluno", content=progress_tab),
            ft.Tab(text="Atualizar Aluno", content=atualizar_tab),
        ]
    )
    
    page.add(tabs)


if __name__ == "__main__":
    ft.app(target=main)