<template>
  <Dialog
    v-model="show"
    :options="{
      title: __('Quick Reminder'),
      size: 'xl',
    }"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <FormControl
          v-model="reminder.title"
          :label="__('Title')"
          type="text"
          :placeholder="__('Enter title')"
        />
        
        <div class="grid grid-cols-2 gap-4">
          <FormControl
            v-model="reminder.date"
            :label="__('Date')"
            type="date"
            :placeholder="__('Select date')"
          />
          
          <FormControl
            v-model="reminder.time"
            :label="__('Time')"
            type="time"
            :placeholder="__('Select time')"
          />
        </div>
        
        <FormControl
          v-model="reminder.remarks"
          :label="__('Remarks')"
          type="textarea"
          :placeholder="__('Add remarks...')"
          :rows="3"
        />
      </div>
    </template>
    
    <template #actions>
      <Button
        variant="solid"
        :label="__('Save')"
        :loading="saving"
        @click="save"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, FormControl, Button, call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'created'])

const show = ref(props.modelValue)
const saving = ref(false)

const reminder = ref({
  title: '',
  date: '',
  time: '',
  remarks: '',
})

watch(
  () => props.modelValue,
  (val) => {
    show.value = val
    if (val) {
      reminder.value = {
        title: '',
        date: '',
        time: '',
        remarks: '',
      }
    }
  }
)

watch(show, (val) => {
  emit('update:modelValue', val)
})

async function save() {
  if (!reminder.value.title || !reminder.value.date || !reminder.value.time) {
    window.frappe?.show_alert({
      message: __('Please fill all required fields'),
      indicator: 'red',
    })
    return
  }
  
  saving.value = true
  
  try {
    const dueDate = `${reminder.value.date} ${reminder.value.time}`
    
    await call('frappe.client.insert', {
      doc: {
        doctype: 'CRM Task',
        title: reminder.value.title,
        due_date: dueDate,
        description: reminder.value.remarks,
        status: 'Backlog',
        priority: 'Medium',
      },
    })
    
    window.frappe?.show_alert({
      message: __('Reminder created successfully'),
      indicator: 'green',
    })
    
    show.value = false
    emit('created')
  } catch (error) {
    console.error('Error creating reminder:', error)
    window.frappe?.show_alert({
      message: __('Failed to create reminder'),
      indicator: 'red',
    })
  } finally {
    saving.value = false
  }
}
</script>

