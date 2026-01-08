<template>
  <LayoutHeader>
    <template #left-header>
      <Breadcrumbs :items="[{ label: __('Calendar'), route: { name: 'Calendar' } }]" />
    </template>
    <template #right-header>
      <Button
        variant="solid"
        :label="__('Create Reminder')"
        iconLeft="plus"
        @click="showQuickReminderModal = true"
      />
    </template>
  </LayoutHeader>
  
  <div class="flex flex-col h-full overflow-hidden">
    <div class="p-5 border-b flex items-center justify-between">
      <div class="flex items-center gap-4">
        <Button
          icon="chevron-left"
          variant="ghost"
          @click="previousMonth"
        />
        <h2 class="text-2xl font-semibold">
          {{ currentMonthYear }}
        </h2>
        <Button
          icon="chevron-right"
          variant="ghost"
          @click="nextMonth"
        />
        <Button
          :label="__('Today')"
          variant="outline"
          @click="goToToday"
        />
      </div>
      
      <div class="flex items-center gap-2">
        <Badge
          :label="`${tasksResource.data?.length || 0} ${__('Reminders')}`"
          variant="subtle"
          theme="blue"
        />
      </div>
    </div>
    
    <div class="flex-1 overflow-auto p-5">
      <div v-if="tasksResource.loading" class="flex items-center justify-center h-64">
        <LoadingIndicator class="w-6 h-6" />
      </div>
      
      <div v-else-if="!tasksResource.data?.length" class="flex flex-col items-center justify-center h-64 text-ink-gray-5">
        <CalendarIcon class="h-12 w-12 mb-4" />
        <p class="text-lg font-medium">{{ __('No reminders found') }}</p>
        <p class="text-sm mt-2">{{ __('Create a reminder to get started') }}</p>
      </div>
      
      <div v-else class="grid grid-cols-7 gap-4">
        <!-- Day Headers -->
        <div
          v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"
          :key="day"
          class="text-center font-medium text-ink-gray-7 text-sm py-2"
        >
          {{ __(day) }}
        </div>
        
        <!-- Calendar Days -->
        <div
          v-for="(day, index) in calendarDays"
          :key="index"
          class="border rounded-lg p-2 min-h-[120px]"
          :class="{
            'bg-surface-gray-1': !day.isCurrentMonth,
            'bg-surface-white': day.isCurrentMonth,
            'ring-2 ring-blue-500': day.isToday,
          }"
        >
          <div class="text-sm font-medium mb-2" :class="day.isToday ? 'text-blue-600' : 'text-ink-gray-7'">
            {{ day.date.getDate() }}
          </div>
          
          <div class="space-y-1">
            <div
              v-for="task in getTasksForDate(day.date)"
              :key="task.name"
              class="text-xs p-1.5 rounded bg-blue-100 text-blue-900 cursor-pointer hover:bg-blue-200 transition-colors"
              @click="viewTask(task)"
            >
              <div class="font-medium truncate">{{ task.title }}</div>
              <div class="text-[10px] opacity-75">{{ formatTime(task.due_date) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <QuickReminderModal
    v-if="showQuickReminderModal"
    v-model="showQuickReminderModal"
    @created="tasksResource.reload()"
  />
  
  <TaskDetailModal
    v-if="showTaskDetailModal"
    v-model="showTaskDetailModal"
    :task="selectedTask"
  />
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import Breadcrumbs from '@/components/ViewBreadcrumbs.vue'
import QuickReminderModal from '@/components/Modals/QuickReminderModal.vue'
import TaskDetailModal from '@/components/Modals/TaskDetailModal.vue'
import CalendarIcon from '@/components/Icons/CalendarIcon.vue'
import { Button, Badge, LoadingIndicator, createResource } from 'frappe-ui'
import { ref, computed, onMounted } from 'vue'
import { formatDate, formatTime } from '@/utils'

const currentDate = ref(new Date())
const showQuickReminderModal = ref(false)
const showTaskDetailModal = ref(false)
const selectedTask = ref(null)

const currentMonthYear = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
  })
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  // Get first day of month
  const firstDay = new Date(year, month, 1)
  const startingDayOfWeek = firstDay.getDay()
  
  // Get last day of month
  const lastDay = new Date(year, month + 1, 0)
  const endingDateOfMonth = lastDay.getDate()
  
  // Get previous month's last few days
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  
  const days = []
  
  // Add previous month's days
  for (let i = startingDayOfWeek - 1; i >= 0; i--) {
    days.push({
      date: new Date(year, month - 1, prevMonthLastDay - i),
      isCurrentMonth: false,
      isToday: false,
    })
  }
  
  // Add current month's days
  const today = new Date()
  for (let i = 1; i <= endingDateOfMonth; i++) {
    const date = new Date(year, month, i)
    days.push({
      date,
      isCurrentMonth: true,
      isToday:
        date.toDateString() === today.toDateString(),
    })
  }
  
  // Add next month's days to complete the grid
  const remainingDays = 42 - days.length // 6 weeks * 7 days
  for (let i = 1; i <= remainingDays; i++) {
    days.push({
      date: new Date(year, month + 1, i),
      isCurrentMonth: false,
      isToday: false,
    })
  }
  
  return days
})

const tasksResource = createResource({
  url: 'frappe.client.get_list',
  params: {
    doctype: 'CRM Task',
    fields: ['name', 'title', 'due_date', 'status', 'priority', 'description', 'reference_doctype', 'reference_docname'],
    filters: [
      ['due_date', 'is', 'set'],
    ],
    order_by: 'due_date asc',
    limit_page_length: 1000,
  },
  auto: true,
})

function getTasksForDate(date) {
  if (!tasksResource.data) return []
  
  const dateStr = date.toISOString().split('T')[0]
  
  return tasksResource.data.filter((task) => {
    if (!task.due_date) return false
    const taskDateStr = new Date(task.due_date).toISOString().split('T')[0]
    return taskDateStr === dateStr
  })
}

function previousMonth() {
  const newDate = new Date(currentDate.value)
  newDate.setMonth(newDate.getMonth() - 1)
  currentDate.value = newDate
}

function nextMonth() {
  const newDate = new Date(currentDate.value)
  newDate.setMonth(newDate.getMonth() + 1)
  currentDate.value = newDate
}

function goToToday() {
  currentDate.value = new Date()
}

function viewTask(task) {
  selectedTask.value = task
  showTaskDetailModal.value = true
}
</script>

