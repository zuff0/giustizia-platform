import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useToast } from '@/hooks/use-toast'

export function ClientModal({ open, onClose, client, onSave }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    document_number: '',
    process_number: '',
    process_year: new Date().getFullYear(),
    notes: ''
  })
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    if (client) {
      setFormData({
        name: client.name || '',
        email: client.email || '',
        phone: client.phone || '',
        document_number: client.document_number || '',
        process_number: client.process_number || '',
        process_year: client.process_year || new Date().getFullYear(),
        notes: client.notes || ''
      })
    } else {
      setFormData({
        name: '',
        email: '',
        phone: '',
        document_number: '',
        process_number: '',
        process_year: new Date().getFullYear(),
        notes: ''
      })
    }
  }, [client, open])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validação básica
    if (!formData.name || !formData.process_number || !formData.process_year) {
      toast({
        title: "Erro",
        description: "Nome, número do processo e ano são obrigatórios",
        variant: "destructive"
      })
      return
    }

    try {
      setLoading(true)
      
      const url = client ? `/api/clients/${client.id}` : '/api/clients'
      const method = client ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      
      const data = await response.json()
      
      if (data.success) {
        toast({
          title: "Sucesso",
          description: client ? "Cliente atualizado com sucesso" : "Cliente criado com sucesso"
        })
        onSave()
        onClose()
      } else {
        toast({
          title: "Erro",
          description: data.error || "Falha ao salvar cliente",
          variant: "destructive"
        })
      }
    } catch (error) {
      console.error('Erro ao salvar cliente:', error)
      toast({
        title: "Erro",
        description: "Erro de conexão",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>
            {client ? 'Editar Cliente' : 'Adicionar Cliente'}
          </DialogTitle>
          <DialogDescription>
            {client ? 'Atualize as informações do cliente' : 'Adicione um novo cliente ao sistema'}
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">Nome *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleChange('name', e.target.value)}
                placeholder="Nome completo do cliente"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="email@exemplo.com"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="phone">Telefone</Label>
              <Input
                id="phone"
                value={formData.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                placeholder="+55 11 99999-9999"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="document_number">Documento</Label>
              <Input
                id="document_number"
                value={formData.document_number}
                onChange={(e) => handleChange('document_number', e.target.value)}
                placeholder="CPF, RG ou outro documento"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="process_number">Número do Processo *</Label>
              <Input
                id="process_number"
                value={formData.process_number}
                onChange={(e) => handleChange('process_number', e.target.value)}
                placeholder="Ex: 12345"
                required
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="process_year">Ano do Processo *</Label>
              <Input
                id="process_year"
                type="number"
                min="2000"
                max="2030"
                value={formData.process_year}
                onChange={(e) => handleChange('process_year', parseInt(e.target.value))}
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Observações</Label>
            <Textarea
              id="notes"
              value={formData.notes}
              onChange={(e) => handleChange('notes', e.target.value)}
              placeholder="Observações adicionais sobre o cliente ou processo"
              rows={3}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Salvando...' : (client ? 'Atualizar' : 'Criar')}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

