import { defineStore } from 'pinia'
import { useToast } from "primevue/usetoast";

export const useToastStore = defineStore('toast', {
  state: () => ({
    toast: useToast(),
    allToasts : []
  }),
  getters: {
    getToasts(state) { return state.allToasts}
  },
  actions: {
    showSuccess(message) {
       this.toast.add({ severity: 'success', summary: "Success", detail: message, life: 3000 })
       this.allToasts.push({ severity: 'success', summary: "Success", detail: message, timestamp: Date() })
      },
    showInfo(message) {
       this.toast.add({ severity: 'info', summary: "Info", detail: message, life: 3000 })
       this.allToasts.push({ severity: 'info', summary: "Info", detail: message, timestamp: Date() })
      },
    showError(message){
      this.toast.add({ severity: 'error', summary: "Error", detail: message, life: 3000 })
      this.allToasts.push({ severity: 'error', summary: "Error", detail: message, timestamp: Date() })
    }
  }
})
