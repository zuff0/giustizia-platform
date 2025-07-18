// Hook simples para toast notifications
export function useToast() {
  const toast = ({ title, description, variant = 'default' }) => {
    // Implementação simples usando alert por enquanto
    // Em produção, seria substituído por uma biblioteca de toast
    const message = description ? `${title}: ${description}` : title
    
    if (variant === 'destructive') {
      alert(`❌ ${message}`)
    } else {
      alert(`✅ ${message}`)
    }
  }

  return { toast }
}

