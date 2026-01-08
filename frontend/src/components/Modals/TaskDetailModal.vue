<template>
  <Dialog
    v-model="show"
    :options="{
      title: task?.title || __('Task Details'),
      size: 'xl',
    }"
  >
    <template #body-content>
      <div v-if="task" class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-ink-gray-7 mb-1">
            {{ __('Status') }}
          </label>
          <Badge
            :label="task.status"
            :theme="getStatusColor(task.status)"
            variant="subtle"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-ink-gray-7 mb-1">
            {{ __('Priority') }}
          </label>
          <Badge
            :label="task.priority"
            :theme="getPriorityColor(task.priority)"
            variant="subtle"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-ink-gray-7 mb-1">
            {{ __('Due Date') }}
          </label>
          <div class="text-base">
            {{ formatDateTime(task.due_date) }}
          </div>
        </div>
        
        <div v-if="task.reference_doctype && task.reference_docname">
          <label class="block text-sm font-medium text-ink-gray-7 mb-1">
            {{ __('Related To') }}
          </label>
          <div class="text-base">
            {{ task.reference_doctype }}: {{ task.reference_docname }}
          </div>
        </div>
        
        <div v-if="task.description">
          <label class="block text-sm font-medium text-ink-gray-7 mb-1">
            {{ __('Description') }}
          </label>
          <div class="text-base whitespace-pre-wrap">
            {{ task.description }}
          </div>
        </div>
      </div>
    </template>
    
    <template #actions>
      <Button
        variant="solid"
        :label="__('Close')"
        @click="show = false"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, Badge, Button } from 'frappe-ui'
import { formatDate } from '@/utils'

const props = defineProps({
  task: {
    type: Object,
    default: null,
  },
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue'])

const show = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    show.value = val
  }
)

watch(show, (val) => {
  emit('update:modelValue', val)
})

function getStatusColor(status) {
  const colors = {
    'Backlog': 'gray',
    'In Progress': 'blue',
    'Completed': 'green',
    'Cancelled': 'red',
  }
  return colors[status] || 'gray'
}

function getPriorityColor(priority) {
  const colors = {
    'Low': 'gray',
    'Medium': 'yellow',
    'High': 'orange',
    'Critical': 'red',
  }
  return colors[priority] || 'gray'
}

function formatDateTime(dateTime) {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

