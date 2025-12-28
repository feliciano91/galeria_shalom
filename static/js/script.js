document.addEventListener('DOMContentLoaded', function () {

    const btnPrev = document.getElementById('btn_prev');
    const btnNext = document.getElementById('btn_next');
    const mesElement = document.getElementById('mes');
    const anoElement = document.getElementById('ano');

    const diasElement = document.getElementById('datas'); // TBODY do calendário
    const horariosElement = document.getElementById('horarios'); // TBODY horários

    const btnAgendar = document.getElementById('btn-agendar');
    const radiosPagamento = document.querySelectorAll('input[name="pagamento"]');

    const inputData = document.getElementById('dataSelecionada');
    const inputHorario = document.getElementById('horarioSelecionado');

    let dataAtual = new Date();
    let dataSelecionada = null;
    let horarioSelecionado = false;
    let pagamentoSelecionado = false;

    /* ================= CALENDÁRIO ================= */

    function atualizarCalendario() {
        const mesAtual = dataAtual.getMonth();
        const anoAtual = dataAtual.getFullYear();

        mesElement.innerText = dataAtual.toLocaleString('pt-BR', { month: 'long' });
        anoElement.innerText = anoAtual;

        const primeiroDia = new Date(anoAtual, mesAtual, 1).getDay();
        const diasNoMes = new Date(anoAtual, mesAtual + 1, 0).getDate();

        diasElement.innerHTML = '';

        let tr = document.createElement('tr');

        for (let i = 0; i < primeiroDia; i++) {
            tr.appendChild(document.createElement('td'));
        }

        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);

        for (let dia = 1; dia <= diasNoMes; dia++) {
            const td = document.createElement('td');
            td.innerText = dia;
            td.classList.add('dia');

            const dataDia = new Date(anoAtual, mesAtual, dia);
            dataDia.setHours(0, 0, 0, 0);

            if (dataDia < hoje) {
                td.classList.add('past-date');
            } else {
                td.addEventListener('click', () => selecionarDia(dia));
            }

            if (
                dataSelecionada &&
                dataSelecionada.getDate() === dia &&
                dataSelecionada.getMonth() === mesAtual &&
                dataSelecionada.getFullYear() === anoAtual
            ) {
                td.classList.add('selecionado');
            }

            tr.appendChild(td);

            if (tr.children.length === 7) {
                diasElement.appendChild(tr);
                tr = document.createElement('tr');
            }
        }

        if (tr.children.length) {
            diasElement.appendChild(tr);
        }
    }

    function selecionarDia(dia) {
        dataSelecionada = new Date(dataAtual.getFullYear(), dataAtual.getMonth(), dia);
        inputData.value = dataSelecionada.toISOString().split('T')[0];

        horarioSelecionado = false;
        inputHorario.value = '';

        atualizarCalendario();
        preencherHorarios();
        verificarFormulario();
    }

    /* ================= HORÁRIOS ================= */

    function gerarHorarios(inicio, fim, lista) {
        let h = inicio;
        let m = 0;

        while (h < fim || (h === fim && m === 0)) {
            lista.push(`${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`);
            m += 30;
            if (m === 60) {
                m = 0;
                h++;
            }
        }
    }

    function preencherHorarios() {
        horariosElement.innerHTML = '';

        if (!dataSelecionada) return;

        const diaSemana = dataSelecionada.getDay();
        let horarios = [];

        if (diaSemana === 0) {
            horariosElement.innerHTML = '<tr><td>FECHADO</td></tr>';
            return;
        }

        if (diaSemana === 6) {
            gerarHorarios(8, 12, horarios);
        } else {
            gerarHorarios(8, 12, horarios);
            gerarHorarios(14, 18, horarios);
        }

        fetch(`/get_horarios/${inputData.value}`)
            .then(res => res.json())
            .then(ocupados => {

                const horariosOcupados = ocupados.map(h => h.horario.slice(0, 5));
                let tr;

                horarios.forEach((hora, index) => {

                    if (index % 6 === 0) tr = document.createElement('tr');

                    const td = document.createElement('td');
                    td.innerText = hora;

                    if (horariosOcupados.includes(hora)) {
                        td.classList.add('indisponivel');
                    } else {
                        td.classList.add('horario');
                        td.addEventListener('click', () => selecionarHorario(hora));
                    }

                    tr.appendChild(td);

                    if ((index + 1) % 6 === 0 || index === horarios.length - 1) {
                        horariosElement.appendChild(tr);
                    }
                });
            });
    }

    function selecionarHorario(hora) {
        document.querySelectorAll('.horario').forEach(h => h.classList.remove('selecionado'));

        const selecionado = [...document.querySelectorAll('.horario')]
            .find(h => h.innerText === hora);

        if (selecionado) selecionado.classList.add('selecionado');

        inputHorario.value = hora;
        horarioSelecionado = true;
        verificarFormulario();
    }

    /* ================= FORMULÁRIO ================= */

    function verificarFormulario() {
        btnAgendar.disabled = !(dataSelecionada && horarioSelecionado && pagamentoSelecionado);
    }

    radiosPagamento.forEach(radio => {
        radio.addEventListener('change', () => {
            pagamentoSelecionado = true;
            verificarFormulario();
        });
    });

    btnPrev.addEventListener('click', e => {
        e.preventDefault();
        dataAtual.setMonth(dataAtual.getMonth() - 1);
        atualizarCalendario();
    });

    btnNext.addEventListener('click', e => {
        e.preventDefault();
        dataAtual.setMonth(dataAtual.getMonth() + 1);
        atualizarCalendario();
    });

    atualizarCalendario();
});
