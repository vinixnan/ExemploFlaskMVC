"""Classes de domínio reutilizadas pelo DAO e pelas rotas da primeira aula."""


class Pessoa:
    def __init__(self, nusp, nome, email):
        self.nusp = nusp
        self.nome = nome
        self.email = email


class Aluno(Pessoa):
    def __init__(self, nusp, nome, email, curso, ano_ingresso):
        super().__init__(nusp, nome, email)
        self.curso = curso
        self.ano_ingresso = ano_ingresso

    def to_dict(self):
        return {
            "nusp": self.nusp,
            "nome": self.nome,
            "email": self.email,
            "curso": self.curso,
            "ano_ingresso": self.ano_ingresso,
        }


class Disciplina:
    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome}


class Matricula:
    def __init__(self, id_matricula, aluno, disciplina, periodo, nota, frequencia):
        self.id_matricula = id_matricula
        self.aluno = aluno
        self.disciplina = disciplina
        self.periodo = periodo
        self.nota = nota
        self.frequencia = frequencia

    def to_dict(self):
        return {
            "id_matricula": self.id_matricula,
            "aluno": self.aluno.to_dict(),
            "disciplina": self.disciplina.to_dict(),
            "periodo": self.periodo,
            "nota": self.nota,
            "frequencia": self.frequencia,
        }
