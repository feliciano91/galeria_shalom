document.addEventListener('DOMContentLoaded', function () {
    const btnPrev = document.getElementById('btn_prev');
    const btnNext = document.getElementById('btn_next');
    const mesElement = document.getElementById('mes');
    const anoElement = document.getElementById('ano');
    const diasElement = document.getElementById('data');
    const horarioElement = document.getElementById('horario');
    const btnAgendar = document.getElementById('btn-agendar');
    const radiosPagamento = document.querySelectorAll('input[name="pagamento"]');
    const inputData = document.getElementById('dataSelecionada');
    const inputHorario = document.getElementById('horarioSelecionado');

    let dataAtual = new Date();
    let dataSelecionada = null;
    let horarioSelecionado = false;
    let pagamentoSelecionado = false;

    //-----------------------------------------------------
    function atualizarCalendario() {
        const mesAtual = dataAtual.getMonth();
        const anoAtual = dataAtual.getFullYear();
    
        mesElement.innerText = dataAtual.toLocaleString('pt-BR', { month: 'long' });
        anoElement.innerText = anoAtual;
    
        const primeiroDia = new Date(anoAtual, mesAtual, 1);
        const ultimoDia = new Date(anoAtual, mesAtual + 1, 0);
        const diasNoMes = ultimoDia.getDate();
        const diaDaSemana = primeiroDia.getDay();
    
        diasElement.innerHTML = '';
    
        let tr = document.createElement('tr');
        for (let i = 0; i < diaDaSemana; i++) {
            tr.appendChild(document.createElement('td'));
        }
    
        const hoje = new Date();
        // Ajustando 'hoje' para remover a hora, minuto e segundo
        hoje.setHours(0, 0, 0, 0); // Zera a hora, minuto, segundo e milissegundo
    
        for (let i = 1; i <= diasNoMes; i++) {
            const diaElement = document.createElement('td');
            diaElement.innerText = i;
            diaElement.classList.add('dia');
    
            const dataDia = new Date(anoAtual, mesAtual, i);
            // Ajustando a data para comparar apenas o dia, mês e ano
            dataDia.setHours(0, 0, 0, 0); // Zera a hora, minuto, segundo e milissegundo
    
            // Verifica se a data é anterior à data atual
            if (dataDia < hoje) {
                diaElement.classList.add('past-date');
                diaElement.style.cursor = 'not-allowed'; // Desabilita o clique nas datas passadas
            } else {
                // Se a data for hoje ou no futuro, permite selecionar
                diaElement.addEventListener('click', () => selecionarDia(i));
            }
    
            // Destaca o dia de hoje
            if (hoje.getDate() === i && hoje.getMonth() === mesAtual && hoje.getFullYear() === anoAtual) {
                diaElement.classList.add('hoje');
            }
    
            // Destaca o dia selecionado
            if (dataSelecionada && dataSelecionada.getDate() === i && dataSelecionada.getMonth() === mesAtual && dataSelecionada.getFullYear() === anoAtual) {
                diaElement.classList.add('selecionado');
            }
    
            tr.appendChild(diaElement);
    
            if (tr.children.length === 7) {
                diasElement.appendChild(tr);
                tr = document.createElement('tr');
            }
        }
    
        if (tr.children.length > 0) {
            diasElement.appendChild(tr);
        }
    }
    
    // Função para selecionar o dia
    function selecionarDia(dia) {
        dataSelecionada = new Date(dataAtual.getFullYear(), dataAtual.getMonth(), dia);
        inputData.value = dataSelecionada.toISOString().split('T')[0]; // Preenche o campo de data invisível
        horarioSelecionado = false;
        atualizarCalendario();
        preencherHorarios();  // Preenche os horários após a seleção de data
        verificarFormulario();
    }
//==================================================

    // Função para preencher os horários
    function preencherHorarios() {
        horarioElement.innerHTML = ''; // Limpa os horários anteriores
        const diaSemana = dataSelecionada.getDay(); // Pega o dia da semana (0 = domingo, 6 = sábado)

        let horariosDisponiveis = [];
        let horaAtual = 8;
        let minutoAtual = 0;

        // Preenche os horários dependendo do dia da semana
        if (diaSemana === 6) {  // Se for sábado
            // Preenche os horários das 08:00 às 12:00 para o sábado
            while (horaAtual < 12 || (horaAtual === 12 && minutoAtual === 0)) {
                let horaFormatada = horaAtual.toString().padStart(2, '0');
                let minutoFormatado = minutoAtual.toString().padStart(2, '0');
                horariosDisponiveis.push(`${horaFormatada}:${minutoFormatado}`);
                
                // Avança 30 minutos
                minutoAtual += 30;
                if (minutoAtual === 60) {
                    minutoAtual = 0;
                    horaAtual += 1;
                }
            }
        } else if (diaSemana === 0) {  // Se for domingo
            horarioElement.innerHTML = '<p>FECHADO</p>';
            return;
        } else {  // De segunda a sexta-feira
            // Preenche os horários das 08:00 às 12:00
            while (horaAtual < 12 || (horaAtual === 12 && minutoAtual === 0)) {
                let horaFormatada = horaAtual.toString().padStart(2, '0');
                let minutoFormatado = minutoAtual.toString().padStart(2, '0');
                horariosDisponiveis.push(`${horaFormatada}:${minutoFormatado}`);
                
                // Avança 30 minutos
                minutoAtual += 30;
                if (minutoAtual === 60) {
                    minutoAtual = 0;
                    horaAtual += 1;
                }
            }

            // Preenche os horários das 14:00 às 18:00
            horaAtual = 14;
            minutoAtual = 0;

            while (horaAtual < 18 || (horaAtual === 18 && minutoAtual === 0)) {
                let horaFormatada = horaAtual.toString().padStart(2, '0');
                let minutoFormatado = minutoAtual.toString().padStart(2, '0');
                horariosDisponiveis.push(`${horaFormatada}:${minutoFormatado}`);
                
                // Avança 30 minutos
                minutoAtual += 30;
                if (minutoAtual === 60) {
                    minutoAtual = 0;
                    horaAtual += 1;
                }
            }
        }
    
        // Busca os horários podologo já agendados no banco de dados
        fetch(`/get_horariop/${dataSelecionada.toISOString().split('T')[0]}`)
            .then(response => response.json())
            .then(horariosOcupados => {
                console.log('Horários ocupados recebidos do backend:', horariosOcupados);

                // ✅ Converte os objetos recebidos (com campo "horario") em strings no formato "HH:MM"
                const horariosOcupadosFormatados = horariosOcupados.map(h => h.horario.slice(0, 5));
                console.log('Horários ocupados formatados:', horariosOcupadosFormatados);

                // Exibe os horários em linhas com 6 colunas
                for (let i = 0; i < horariosDisponiveis.length; i++) {
                    if (i % 6 === 0) {
                        var tr = document.createElement('tr'); // nova linha
                    }

                    const td = document.createElement('td');
                    td.innerText = horariosDisponiveis[i];

                    // Verifica se o horário está ocupado
                    if (horariosOcupadosFormatados.includes(horariosDisponiveis[i])) {
                        td.classList.add('indisponivel'); // aplica estilo para horários ocupados
                        console.log(`${horariosDisponiveis[i]} está OCUPADO`);
                    } else {
                        td.classList.add('horario');
                        td.addEventListener('click', () => selecionarHorario(horariosDisponiveis[i])); // clique no horário disponível
                    }

                    tr.appendChild(td);

                    if ((i + 1) % 6 === 0 || i === horariosDisponiveis.length - 1) {
                        horarioElement.appendChild(tr); // adiciona a linha à tabela
                    }
                }
            })
            .catch(error => console.error('Erro ao buscar horários:', error));
        }
    

    // Função para selecionar o horário
    function selecionarHorario(hora) {
        // Limpa a seleção anterior
        const horarios = document.querySelectorAll('.horario');
        horarios.forEach(h => h.classList.remove('selecionado'));

        // Adiciona a classe de destaque no horário selecionado
        const horarioElement = Array.from(document.querySelectorAll('.horario'))
            .find(h => h.innerText === hora);
        
        if (horarioElement) {
            horarioElement.classList.add('selecionado');
        }

        inputHorario.value = hora;
        horarioSelecionado = true;
        verificarFormulario();
    }

    // Função para verificar se todos os campos estão preenchidos
    function verificarFormulario() {
        if (dataSelecionada && horarioSelecionado && pagamentoSelecionado) {
            btnAgendar.disabled = false;  // Habilita o botão de agendamento
        } else {
            btnAgendar.disabled = true;   // Desabilita o botão de agendamento
        }
    }

    // Função para ativar o pagamento
    radiosPagamento.forEach(radio => {
        radio.addEventListener('change', () => {
            pagamentoSelecionado = true;
            verificarFormulario();
        });
    });

    // Função para mover o calendário para o mês anterior
    btnPrev.addEventListener('click', function (event) {
        event.preventDefault(); // Impede o comportamento padrão de navegação
        dataAtual.setMonth(dataAtual.getMonth() - 1);  // Subtrai 1 do mês
        atualizarCalendario();  // Atualiza o calendário
    });

    // Função para mover o calendário para o próximo mês
    btnNext.addEventListener('click', function (event) {
        event.preventDefault(); // Impede o comportamento padrão de navegação
        dataAtual.setMonth(dataAtual.getMonth() + 1);  // Adiciona 1 ao mês
        atualizarCalendario();  // Atualiza o calendário
    });

    // Inicializa o calendário e horários
    atualizarCalendario();
});


