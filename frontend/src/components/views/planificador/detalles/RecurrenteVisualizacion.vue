<template>
<div class="recurrente-visualizacion" v-if="recurrencia">
    <h4>Recurrencia:</h4>
    <p>
    <strong>Tipo:</strong> {{ recurrencia.tipo }}
    </p>
    <p v-if="recurrencia.frecuencia">
    <strong>Frecuencia:</strong> Cada {{ recurrencia.frecuencia }}
    {{ getUnidadTiempo(recurrencia.tipo, recurrencia.frecuencia) }}
    </p>
    <p v-if="recurrencia.dias_semana">
    <strong>Días de la semana:</strong>
    {{ formatDiasSemana(recurrencia.dias_semana) }}
    </p>
    <p v-if="recurrencia.dia_mes">
    <strong>Día del mes:</strong> {{ recurrencia.dia_mes }}
    </p>
    <p v-if="recurrencia.fecha_fin">
    <strong>Fecha de finalización:</strong>
    {{ formatFecha(recurrencia.fecha_fin) }}
    </p>
</div>
<div v-else>
    <p>No hay recurrencia configurada.</p>
</div>
</template>

<script>
export default {
props: {
    recurrencia: {
    type: Object,
    required: false, // Podría ser opcional
    default: null,
    },
},
methods: {
    formatFecha(fecha) {
    if (!fecha) return "";
    const date = new Date(fecha);
    const options = { year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString("es-ES", options);
    },
    getUnidadTiempo(tipo, frecuencia) {
    if (tipo === "diario") {
        return frecuencia === 1 ? "día" : "días";
    } else if (tipo === "semanal") {
        return frecuencia === 1 ? "semana" : "semanas";
    } else if (tipo === "mensual") {
        return frecuencia === 1 ? "mes" : "meses";
    } else if (tipo === "anual") {
        return frecuencia === 1 ? "año" : "años";
    } else {
        return "";
    }
    },
    formatDiasSemana(dias) {
        if(!dias) return "";
    const diasSemana = {
        0: "Domingo",
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
    };
    const diasSeleccionados = dias
        .map((dia) => diasSemana[dia])
        .join(", ");
    return diasSeleccionados;
    },
},
};
</script>

<style scoped>
.recurrente-visualizacion {
border: 1px solid #ccc;
border-radius: 5px;
padding: 10px;
margin-bottom: 10px;
background-color: #f8f8f8;
}

.recurrente-visualizacion h4 {
margin-top: 0;
}

.recurrente-visualizacion p {
margin: 5px 0;
}
</style>