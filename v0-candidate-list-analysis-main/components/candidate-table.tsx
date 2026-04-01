"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight, RefreshCw, Plus } from "lucide-react"

const candidateData = [
  {
    no: 1,
    candidato: "172",
    cantTicket: 89,
    ventaNro: 205.5,
    maxJugada: 15.0,
    montoPrem: 143850.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 60,
    ventaAsoc: 263.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 15780.0,
    porcPremAsoc: 35,
  },
  {
    no: 2,
    candidato: "280",
    cantTicket: 88,
    ventaNro: 198.75,
    maxJugada: 15.0,
    montoPrem: 139125.0,
    porcPrem: 33,
    precaucion: "ALERTA",
    cantTicketAsoc: 41,
    ventaAsoc: 138.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 8310.0,
    porcPremAsoc: 19,
  },
  {
    no: 3,
    candidato: "727",
    cantTicket: 82,
    ventaNro: 197.2,
    maxJugada: 10.0,
    montoPrem: 138040.0,
    porcPrem: 33,
    precaucion: "ALERTA",
    cantTicketAsoc: 178,
    ventaAsoc: 610.19,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 36611.4,
    porcPremAsoc: 82,
  },
  {
    no: 4,
    candidato: "900",
    cantTicket: 81,
    ventaNro: 207.7,
    maxJugada: 20.0,
    montoPrem: 145390.0,
    porcPrem: 35,
    precaucion: "ALERTA",
    cantTicketAsoc: 148,
    ventaAsoc: 517.83,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 31069.8,
    porcPremAsoc: 69,
  },
  {
    no: 5,
    candidato: "687",
    cantTicket: 78,
    ventaNro: 202.7,
    maxJugada: 12.0,
    montoPrem: 141890.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 62,
    ventaAsoc: 406.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 24360.0,
    porcPremAsoc: 54,
  },
  {
    no: 6,
    candidato: "508",
    cantTicket: 75,
    ventaNro: 201.0,
    maxJugada: 15.0,
    montoPrem: 140700.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 89,
    ventaAsoc: 367.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 22020.0,
    porcPremAsoc: 49,
  },
  {
    no: 7,
    candidato: "481",
    cantTicket: 73,
    ventaNro: 186.25,
    maxJugada: 10.0,
    montoPrem: 130375.0,
    porcPrem: 31,
    precaucion: "ALERTA",
    cantTicketAsoc: 89,
    ventaAsoc: 383.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 22980.0,
    porcPremAsoc: 51,
  },
  {
    no: 8,
    candidato: "289",
    cantTicket: 71,
    ventaNro: 208.05,
    maxJugada: 30.0,
    montoPrem: 145635.0,
    porcPrem: 35,
    precaucion: "ALERTA",
    cantTicketAsoc: 51,
    ventaAsoc: 365.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 21930.0,
    porcPremAsoc: 49,
  },
  {
    no: 9,
    candidato: "697",
    cantTicket: 71,
    ventaNro: 192.5,
    maxJugada: 30.0,
    montoPrem: 134750.0,
    porcPrem: 32,
    precaucion: "ALERTA",
    cantTicketAsoc: 52,
    ventaAsoc: 413.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 24780.0,
    porcPremAsoc: 55,
  },
  {
    no: 10,
    candidato: "430",
    cantTicket: 71,
    ventaNro: 181.0,
    maxJugada: 10.0,
    montoPrem: 126700.0,
    porcPrem: 30,
    precaucion: "ALERTA",
    cantTicketAsoc: 70,
    ventaAsoc: 254.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 15240.0,
    porcPremAsoc: 34,
  },
  {
    no: 11,
    candidato: "380",
    cantTicket: 70,
    ventaNro: 207.25,
    maxJugada: 25.0,
    montoPrem: 145075.0,
    porcPrem: 35,
    precaucion: "ALERTA",
    cantTicketAsoc: 41,
    ventaAsoc: 138.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 8310.0,
    porcPremAsoc: 19,
  },
  {
    no: 12,
    candidato: "978",
    cantTicket: 70,
    ventaNro: 199.7,
    maxJugada: 10.0,
    montoPrem: 139790.0,
    porcPrem: 33,
    precaucion: "ALERTA",
    cantTicketAsoc: 49,
    ventaAsoc: 239.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 14370.0,
    porcPremAsoc: 32,
  },
  {
    no: 13,
    candidato: "848",
    cantTicket: 69,
    ventaNro: 203.0,
    maxJugada: 20.0,
    montoPrem: 142100.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 273,
    ventaAsoc: 968.35,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 58101.0,
    porcPremAsoc: 130,
  },
  {
    no: 14,
    candidato: "187",
    cantTicket: 69,
    ventaNro: 197.5,
    maxJugada: 20.0,
    montoPrem: 138250.0,
    porcPrem: 33,
    precaucion: "ALERTA",
    cantTicketAsoc: 62,
    ventaAsoc: 406.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 24360.0,
    porcPremAsoc: 54,
  },
  {
    no: 15,
    candidato: "857",
    cantTicket: 67,
    ventaNro: 193.0,
    maxJugada: 50.0,
    montoPrem: 135100.0,
    porcPrem: 32,
    precaucion: "ALERTA",
    cantTicketAsoc: 76,
    ventaAsoc: 301.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 18090.0,
    porcPremAsoc: 40,
  },
  {
    no: 16,
    candidato: "780",
    cantTicket: 67,
    ventaNro: 201.0,
    maxJugada: 25.0,
    montoPrem: 140700.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 41,
    ventaAsoc: 138.5,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 8310.0,
    porcPremAsoc: 19,
  },
  {
    no: 17,
    candidato: "808",
    cantTicket: 66,
    ventaNro: 204.0,
    maxJugada: 20.0,
    montoPrem: 142800.0,
    porcPrem: 34,
    precaucion: "ALERTA",
    cantTicketAsoc: 89,
    ventaAsoc: 367.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 22020.0,
    porcPremAsoc: 49,
  },
  {
    no: 18,
    candidato: "897",
    cantTicket: 66,
    ventaNro: 193.5,
    maxJugada: 15.0,
    montoPrem: 135450.0,
    porcPrem: 32,
    precaucion: "ALERTA",
    cantTicketAsoc: 52,
    ventaAsoc: 413.0,
    maxJugadaAsoc: 50.0,
    montoPremAsoc: 24780.0,
    porcPremAsoc: 55,
  },
]

export function CandidateTable() {
  const [selectedRows, setSelectedRows] = useState<number[]>([])

  const formatNumber = (num: number, decimals = 2) => {
    return num.toLocaleString("es-ES", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
  }

  const toggleRow = (no: number) => {
    setSelectedRows((prev) => (prev.includes(no) ? prev.filter((n) => n !== no) : [...prev, no]))
  }

  return (
    <div className="font-sans text-sm">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 text-xs text-gray-700">
        <span className="font-semibold">SELECCION DE CANDIDATOS</span>
        <span>19/3/15 17:19</span>
      </div>

      {/* Configuration box */}
      <div className="border border-gray-400 p-2 mb-6 text-sm text-gray-700">
        Configuración de Sorteos Digitales por día.
      </div>

      {/* Date */}
      <div className="text-right mb-4">
        <span className="text-gray-700">Fecha: </span>
        <span className="text-green-700 underline">Jueves, 19 de Marzo de 2015</span>
      </div>

      {/* Title */}
      <h1 className="text-center text-xl font-bold underline mb-6 text-gray-800">LISTADO DE NÚMEROS CANDIDATOS</h1>

      {/* Sorteo Info */}
      <div className="mb-4">
        <span className="text-red-600">Sorteo: </span>
        <span className="text-green-700 text-2xl font-semibold">TRIPLE TÁCHIRA 5:00 PM</span>
        <span className="text-gray-700">, </span>
        <span className="text-red-600">Lista: </span>
        <span className="text-green-700 font-semibold">TRIPLE</span>
        <span className="text-gray-700">, </span>
        <span className="text-red-600">Tipo Lista: </span>
        <span className="text-gray-800 text-lg font-semibold">LISTA B</span>
      </div>

      {/* Estado del Sorteo */}
      <div className="flex justify-center gap-16 mb-4 text-sm">
        <div>
          <span className="text-gray-700">Estado del Sorteo: </span>
          <span className="text-green-700 underline font-semibold">ABIERTO</span>
        </div>
        <div>
          <span className="text-gray-700">Ultimo análisis: </span>
          <span className="text-red-600 underline">16:05:27</span>
          <span className="text-gray-700 underline"> hrs.</span>
        </div>
      </div>

      {/* Seleccionar Número Button */}
      <div className="flex justify-center mb-6">
        <Button variant="outline" className="border-gray-400 text-gray-700 px-6 bg-transparent">
          Seleccionar Número
        </Button>
      </div>

      {/* Results header */}
      <div className="border border-gray-400">
        {/* Top bar */}
        <div className="flex justify-between items-center px-2 py-1 border-b border-gray-400 bg-white">
          <span className="font-semibold text-gray-800">Resultados de la búsqueda</span>
          <div className="flex items-center gap-4">
            <div className="flex gap-1">
              <button className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white">
                <RefreshCw className="w-3 h-3" />
              </button>
              <button className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white">
                <Plus className="w-3 h-3" />
              </button>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <button className="text-gray-600 hover:text-gray-800">
                <ChevronsLeft className="w-4 h-4" />
              </button>
              <button className="text-gray-600 hover:text-gray-800">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span>1 de 1</span>
              <button className="text-gray-600 hover:text-gray-800">
                <ChevronRight className="w-4 h-4" />
              </button>
              <button className="text-gray-600 hover:text-gray-800">
                <ChevronsRight className="w-4 h-4" />
              </button>
              <span className="ml-2">47 filas</span>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-xs border-collapse">
            <thead>
              {/* Header groups */}
              <tr className="bg-gray-100">
                <th colSpan={8} className="border border-gray-400 py-1 text-center font-semibold">
                  Lista Principal Analizada
                </th>
                <th colSpan={6} className="border border-gray-400 py-1 text-center font-semibold">
                  Lista Asociada
                </th>
              </tr>
              {/* Column headers */}
              <tr className="bg-gray-50">
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">No.</th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">Selección</th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">Candidato</th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Cant.
                  <br />
                  Ticket
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Venta
                  <br />
                  Nro
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Max
                  <br />
                  Jugada
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Monto
                  <br />
                  Premiación
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  %<br />
                  Premiación
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">Precaución</th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Cant.
                  <br />
                  Ticket
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Venta
                  <br />
                  Asoc
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Max
                  <br />
                  Jugada
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  Monto
                  <br />
                  Premiación
                </th>
                <th className="border border-gray-400 px-1 py-1 text-center font-semibold">
                  %<br />
                  Premiación
                </th>
              </tr>
            </thead>
            <tbody>
              {candidateData.map((row) => (
                <tr key={row.no} className="hover:bg-gray-50">
                  <td className="border border-gray-400 px-2 py-1 text-center">{row.no}</td>
                  <td className="border border-gray-400 px-2 py-1 text-center">
                    <Checkbox
                      checked={selectedRows.includes(row.no)}
                      onCheckedChange={() => toggleRow(row.no)}
                      className="h-4 w-4"
                    />
                  </td>
                  <td className="border border-gray-400 px-2 py-1 text-center text-blue-600 font-semibold underline cursor-pointer">
                    {row.candidato}
                  </td>
                  <td className="border border-gray-400 px-2 py-1 text-center">{row.cantTicket}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.ventaNro)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.maxJugada)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.montoPrem)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-center">{row.porcPrem} %</td>
                  <td className="border border-gray-400 px-2 py-1 text-center text-red-600 font-semibold">
                    {row.precaucion}
                  </td>
                  <td className="border border-gray-400 px-2 py-1 text-center">{row.cantTicketAsoc}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.ventaAsoc)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.maxJugadaAsoc)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-right">{formatNumber(row.montoPremAsoc)}</td>
                  <td className="border border-gray-400 px-2 py-1 text-center">{row.porcPremAsoc} %</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
