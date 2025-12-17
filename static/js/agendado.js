document.addEventListener("DOMContentLoaded", function () {
    const calendario = document.getElementById('data');
    const mesElemento = document.getElementById('mes');
    const anoElemento = document.getElementById('ano');
    const horariosTabela = document.getElementById('horario').getElementsByTagName('tbody')[0];
    const dataAtual = new Date();
    // Variáveis globais para o ano e mês atuais

    let anoAtual = dataAtual.getFullYear(); // Obtém o ano atual
    let mesAtual = dataAtual.getMonth(); // Obtém o mês atual (0-11, onde 0 é janeiro)

   // Função para gerar o calendário
    function gerarCalendario() {
        const primeiroDiaDoMes = new Date(anoAtual, mesAtual, 1);
        const diasNoMes = new Date(anoAtual, mesAtual + 1, 0).getDate();
        const primeiroDiaDaSemana = primeiroDiaDoMes.getDay(); // 0 = Domingo, 1 = Segunda, etc.

        // Limpa o conteúdo atual do calendário
        calendario.innerHTML = '';
        mesElemento.innerText = new Date(anoAtual, mesAtual).toLocaleString('default', { month: 'long' });
        anoElemento.innerText = anoAtual;

        let linha = document.createElement('tr');
        // Preenche os espaços vazios antes do primeiro dia do mês
        for (let i = 0; i < primeiroDiaDaSemana; i++) {
            let td = document.createElement('td');
            linha.appendChild(td);
        }

        const dataHoje = new Date();
        const dataHojeFormatada = `${dataHoje.getFullYear()}-${String(dataHoje.getMonth() + 1).padStart(2, '0')}-${String(dataHoje.getDate()).padStart(2, '0')}`;

        for (let dia = 1; dia <= diasNoMes; dia++) {
            // Cria uma nova linha quando houver 7 células
            if (linha.children.length === 7) {
                calendario.appendChild(linha);
                linha = document.createElement('tr');
            }

            let td = document.createElement('td');
            td.innerText = dia;
            td.classList.add('dia');

            // Verifica se a data atual é igual ao dia da célula e destaca
            const dataDia = `${anoAtual}-${String(mesAtual + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;
            if (dataDia === dataHojeFormatada) {
                td.classList.add('data-hoje'); // Destaca a data atual
            }

            td.addEventListener('click', () => mostrarHorarios(dia));
            linha.appendChild(td);
        }

        // Adiciona a última linha do mês ao calendário
        calendario.appendChild(linha);
    }

    // Função para mostrar os horários disponíveis para a data clicada
    function mostrarHorarios(dia) {
        const dataSelecionada = `${anoAtual}-${String(mesAtual + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;

        fetch(`/get_horarios/${dataSelecionada}`)
            .then(response => response.json())
            .then(agendamentos => {
                horariosTabela.innerHTML = ''; // Limpa os horários anteriores

                if (agendamentos.length === 0) {
                    let tr = document.createElement("tr");
                    let td = document.createElement("td");
                    td.colSpan = 5; // agora são 5 colunas
                    td.innerText = "Nenhum horário agendado nessa data";
                    tr.appendChild(td);
                    horariosTabela.appendChild(tr);
                } else {
                    // Cabeçalho da tabela (opcional)
                    let header = document.createElement("tr");
                    header.innerHTML = `
                        <th>Nome</th>
                        <th>Contato</th>
                        <th>Horário</th>
                        <th>Pagamento</th>
                        <th>Serviço</th>
                    `;
                    horariosTabela.appendChild(header);

                    agendamentos.forEach(function (item) {
                        let tr = document.createElement("tr");
                        tr.innerHTML = `
                            <td>${item.nome}</td>
                            <td>${item.contato}</td>
                            <td>${item.horario}</td>
                            <td>${item.pagamento}</td>
                            <td>${item.servico}</td>
                        `;
                        horariosTabela.appendChild(tr);
                    });
                }
            })
            .catch(error => console.error("Erro ao buscar horários:", error));
    }



    
    // Navegação no calendário
    document.getElementById('btn_prev').addEventListener('click', () => {
        mesAtual--;
        if (mesAtual < 0) {
            mesAtual = 11;
            anoAtual--;
        }
        gerarCalendario();
    });

    document.getElementById('btn_next').addEventListener('click', () => {
        mesAtual++;
        if (mesAtual > 11) {
            mesAtual = 0;
            anoAtual++;
        }
        gerarCalendario();
    });

    gerarCalendario(); // Inicializa o calendário
});
