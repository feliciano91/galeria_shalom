$(document).ready(function() {
    // Inicializando o FullCalendar
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: '/get_agendamentomanicure',  // A URL que irá fornecer os eventos (JSON)
        eventClick: function(event) {
            // Exibindo informações sobre o evento ao ser clicado
            alert('Evento: ' + event.title + '\nData: ' + event.start.format());
        },
        dayClick: function(date, jsEvent, view) {
            // Quando clicar em uma data, buscamos os horários agendados para essa data
            var selectedDate = date.format('YYYY-MM-DD');  // Data no formato 'YYYY-MM-DD'
            
            // Fazendo a requisição para pegar os horários
            $.ajax({
                url: '/get_horarios/' + selectedDate,  // Envia a data para o servidor
                method: 'GET',
                success: function(horarios) {
                    if (horarios.length > 0) {
                        // Exibindo os horários no modal
                        var horariosList = $('#horarios-list');
                        horariosList.empty();  // Limpa a lista antes de adicionar os novos horários
                        horarios.forEach(function(horario) {
                            horariosList.append('<li>' + horario + '</li>');
                        });
                        $('#myModal').fadeIn();  // Exibe o modal com os horários
                    } else {
                        alert('Não há agendamentos para esta data.');
                    }
                }
            });
        }
    });

    // Fechar o modal
    $('.close').click(function() {
        $('#myModal').fadeOut();
    });
});
