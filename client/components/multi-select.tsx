"use client"

import * as React from "react"
import { X } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

interface MultiSelectProps {
  options: {
    label: string
    value: string
  }[]
  onValueChange: (value: string[]) => void
  defaultValue?: string[]
  placeholder?: string
  variant?: "default" | "inverted"
  maxCount?: number
}

export function MultiSelect({
  options,
  onValueChange,
  defaultValue = [],
  placeholder = "Select items...",
  variant = "default",
  maxCount = 3,
}: MultiSelectProps) {
  const [open, setOpen] = React.useState(false)
  const [selected, setSelected] = React.useState<string[]>(defaultValue)

  const handleUnselect = (item: string) => {
    const newSelected = selected.filter((s) => s !== item)
    setSelected(newSelected)
    onValueChange(newSelected)
  }

  const handleSelect = (item: string) => {
    const newSelected = selected.includes(item) ? selected.filter((s) => s !== item) : [...selected, item]
    setSelected(newSelected)
    onValueChange(newSelected)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <div className="flex min-h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer">
          <div className="flex flex-wrap gap-1">
            {selected.length > 0 ? (
              <>
                {selected.slice(0, maxCount).map((item) => (
                  <Badge variant={variant === "default" ? "secondary" : "default"} key={item} className="mr-1 mb-1">
                    {item}
                    <button
                      className="ml-1 ring-offset-background rounded-full outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          handleUnselect(item)
                        }
                      }}
                      onMouseDown={(e) => {
                        e.preventDefault()
                        e.stopPropagation()
                      }}
                      onClick={() => handleUnselect(item)}
                    >
                      <X className="h-3 w-3 text-muted-foreground hover:text-foreground" />
                    </button>
                  </Badge>
                ))}
                {selected.length > maxCount && (
                  <Badge variant={variant === "default" ? "secondary" : "default"} className="mr-1 mb-1">
                    +{selected.length - maxCount} more
                  </Badge>
                )}
              </>
            ) : (
              <span className="text-muted-foreground">{placeholder}</span>
            )}
          </div>
        </div>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0" align="start">
        <Command>
          <CommandInput placeholder="Search..." />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              {options.map((option) => (
                <CommandItem key={option.value} onSelect={() => handleSelect(option.value)}>
                  <div
                    className={`mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary ${
                      selected.includes(option.value)
                        ? "bg-primary text-primary-foreground"
                        : "opacity-50 [&_svg]:invisible"
                    }`}
                  >
                    <X className="h-2 w-2" />
                  </div>
                  <span>{option.label}</span>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
