export function Separator({ className = '', ...props }) {
  return (
    <div
      className={`border-t border-gray-200 ${className}`}
      {...props}
    />
  )
}

