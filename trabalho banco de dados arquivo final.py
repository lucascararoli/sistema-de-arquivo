import tkinter as tk
from tkinter import messagebox
import psycopg2

# Função para conectar ao banco de dados PostgreSQL
def conectar_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="arquivo",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e.pgcode} - {e.pgerror}")
        return None

# Função para inserir um novo cliente no banco de dados
def inserir_cliente():
    try:
        n_processo = entry_n_processo.get()
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        cidade = entry_cidade.get()
        uf = entry_uf.get()
        data_abertura = entry_data_abertura.get()
        data_fechamento = entry_data_fechamento.get()
        descricao = entry_descricao.get("1.0", tk.END).strip()

        if not n_processo or not nome or not cpf or not data_abertura:
            messagebox.showerror("Erro ao Inserir", "Por favor, preencha todos os campos obrigatórios (Nº Processo, Nome, CPF, Data Abertura).")
            return

        conn = conectar_postgresql()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO clientes (N_processo, nome, cpf, telefone, email, cidade, uf, data_abertura_processo, data_fechamento_processo, descricao_processo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (n_processo, nome, cpf, telefone, email, cidade, uf, data_abertura, data_fechamento, descricao))
                conn.commit()
                messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
                limpar_campos()
            except psycopg2.Error as e:
                messagebox.showerror("Erro ao Inserir", f"Erro ao inserir cliente: {e.pgcode} - {e.pgerror}")
            finally:
                if conn:
                    cur.close()
                    conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para buscar um cliente no banco de dados
def buscar_cliente():
    try:
        n_processo = entry_n_processo.get()

        if not n_processo:
            messagebox.showerror("Erro ao Buscar", "Por favor, insira o Nº do Processo para buscar.")
            return

        conn = conectar_postgresql()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM clientes WHERE N_processo = %s", (n_processo,))
                cliente = cur.fetchone()
                if cliente:
                    # Preencher os campos com os dados do cliente
                    entry_nome.delete(0, tk.END)
                    entry_nome.insert(0, cliente[1])
                    entry_cpf.delete(0, tk.END)
                    entry_cpf.insert(0, cliente[2])
                    entry_telefone.delete(0, tk.END)
                    entry_telefone.insert(0, cliente[3])
                    entry_email.delete(0, tk.END)
                    entry_email.insert(0, cliente[4])
                    entry_cidade.delete(0, tk.END)
                    entry_cidade.insert(0, cliente[5])
                    entry_uf.delete(0, tk.END)
                    entry_uf.insert(0, cliente[6])
                    entry_data_abertura.delete(0, tk.END)
                    entry_data_abertura.insert(0, cliente[7])
                    entry_data_fechamento.delete(0, tk.END)
                    entry_data_fechamento.insert(0, cliente[8])
                    entry_descricao.delete("1.0", tk.END)
                    entry_descricao.insert(tk.END, cliente[9])
                    messagebox.showinfo("Sucesso", "Cliente encontrado!")
                else:
                    messagebox.showinfo("Não Encontrado", "Nenhum cliente encontrado com o Nº de Processo fornecido.")
            except psycopg2.Error as e:
                messagebox.showerror("Erro ao Buscar", f"Erro ao buscar cliente: {e.pgcode} - {e.pgerror}")
            finally:
                if conn:
                    cur.close()
                    conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para atualizar um cliente no banco de dados
def atualizar_cliente():
    try:
        n_processo = entry_n_processo.get()
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        cidade = entry_cidade.get()
        uf = entry_uf.get()
        data_abertura = entry_data_abertura.get()
        data_fechamento = entry_data_fechamento.get()
        descricao = entry_descricao.get("1.0", tk.END).strip()

        if not n_processo:
            messagebox.showerror("Erro ao Atualizar", "Por favor, insira o Nº do Processo para atualizar.")
            return

        conn = conectar_postgresql()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE clientes
                    SET nome = %s, cpf = %s, telefone = %s, email = %s, cidade = %s, uf = %s, data_abertura_processo = %s, data_fechamento_processo = %s, descricao_processo = %s
                    WHERE N_processo = %s
                """, (nome, cpf, telefone, email, cidade, uf, data_abertura, data_fechamento, descricao, n_processo))
                if cur.rowcount == 0:
                    messagebox.showinfo("Não Encontrado", "Nenhum cliente encontrado com o Nº de Processo fornecido.")
                else:
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                    limpar_campos()
            except psycopg2.Error as e:
                messagebox.showerror("Erro ao Atualizar", f"Erro ao atualizar cliente: {e.pgcode} - {e.pgerror}")
            finally:
                if conn:
                    cur.close()
                    conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para excluir um cliente do banco de dados
def excluir_cliente():
    try:
        n_processo = entry_n_processo.get()

        if not n_processo:
            messagebox.showerror("Erro ao Excluir", "Por favor, insira o Nº do Processo para excluir.")
            return

        conn = conectar_postgresql()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM clientes WHERE N_processo = %s", (n_processo,))
                if cur.rowcount == 0:
                    messagebox.showinfo("Não Encontrado", "Nenhum cliente encontrado com o Nº de Processo fornecido.")
                else:
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    limpar_campos()
            except psycopg2.Error as e:
                messagebox.showerror("Erro ao Excluir", f"Erro ao excluir cliente: {e.pgcode} - {e.pgerror}")
            finally:
                if conn:
                    cur.close()
                    conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Função para limpar os campos após a inserção
def limpar_campos():
    entry_n_processo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)
    entry_uf.delete(0, tk.END)
    entry_data_abertura.delete(0, tk.END)
    entry_data_fechamento.delete(0, tk.END)
    entry_descricao.delete("1.0", tk.END)

# Inicializar a interface Tkinter
root = tk.Tk()
root.title("Cadastro de Clientes")

# Criar os widgets de entrada
tk.Label(root, text="Nº Processo:").grid(row=0, column=0, sticky=tk.E)
entry_n_processo = tk.Entry(root, width=20)
entry_n_processo.grid(row=0, column=1, columnspan=3)

tk.Label(root, text="Nome:").grid(row=1, column=0, sticky=tk.E)
entry_nome = tk.Entry(root, width=50)
entry_nome.grid(row=1, column=1, columnspan=3)

tk.Label(root, text="CPF:").grid(row=2, column=0, sticky=tk.E)
entry_cpf = tk.Entry(root, width=15)
entry_cpf.grid(row=2, column=1)

tk.Label(root, text="Telefone:").grid(row=2, column=2, sticky=tk.E)
entry_telefone = tk.Entry(root, width=15)
entry_telefone.grid(row=2, column=3)

tk.Label(root, text="E-mail:").grid(row=3, column=0, sticky=tk.E)
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=3, column=1, columnspan=3)

tk.Label(root, text="Cidade:").grid(row=4, column=0, sticky=tk.E)
entry_cidade = tk.Entry(root, width=30)
entry_cidade.grid(row=4, column=1, columnspan=3)

tk.Label(root, text="UF:").grid(row=5, column=0, sticky=tk.E)
entry_uf = tk.Entry(root, width=5)
entry_uf.grid(row=5, column=1, sticky=tk.W)

tk.Label(root, text="Data Abertura:").grid(row=5, column=2, sticky=tk.E)
entry_data_abertura = tk.Entry(root, width=10)
entry_data_abertura.grid(row=5, column=3)

tk.Label(root, text="Data Fechamento:").grid(row=6, column=0, sticky=tk.E)
entry_data_fechamento = tk.Entry(root, width=10)
entry_data_fechamento.grid(row=6, column=1, sticky=tk.W)

tk.Label(root, text="Descrição do Processo:").grid(row=7, column=0, sticky=tk.E)
entry_descricao = tk.Text(root, width=40, height=5)
entry_descricao.grid(row=7, column=1, columnspan=3)

# Criar os botões para realizar as operações
tk.Button(root, text="Inserir Cliente", command=inserir_cliente).grid(row=8, column=0, pady=10)
tk.Button(root, text="Buscar Cliente", command=buscar_cliente).grid(row=8, column=1)
tk.Button(root, text="Atualizar Cliente", command=atualizar_cliente).grid(row=8, column=2)
tk.Button(root, text="Excluir Cliente", command=excluir_cliente).grid(row=8, column=3)

# Iniciar o loop principal da interface
root.mainloop()
