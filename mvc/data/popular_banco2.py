from data.popular_banco import N_ALUNOS, gerar_dados
from model2.dao import AlunoDAO, DisciplinaDAO, MatriculaDAO


def popular_banco():
    aluno_dao = AlunoDAO()
    disciplina_dao = DisciplinaDAO()
    matricula_dao = MatriculaDAO()

    alunos, disciplinas, matriculas = gerar_dados(N_ALUNOS)
    inseridos = {"alunos": 0, "disciplinas": 0, "matriculas": 0}

    for disciplina in disciplinas:
        if disciplina_dao.buscar(disciplina.codigo) is None:
            disciplina_dao.inserir(disciplina)
            inseridos["disciplinas"] += 1

    for aluno in alunos:
        if aluno_dao.buscar(aluno.nusp) is None:
            aluno_dao.inserir(aluno)
            inseridos["alunos"] += 1

    for matricula in matriculas:
        if matricula_dao.buscar(matricula.id_matricula) is None:
            matricula_dao.inserir(matricula)
            inseridos["matriculas"] += 1

    print("Registros adicionados:", inseridos)
    print(
        "Total no banco:",
        {
            "alunos": aluno_dao.contar(),
            "disciplinas": len(disciplina_dao.listar()),
            "matriculas": len(matricula_dao.listar()),
        },
    )


if __name__ == "__main__":
    popular_banco()
