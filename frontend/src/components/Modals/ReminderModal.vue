<template>
  <Dialog
    v-model="show"
    :options="{
      title: __('Create Reminder'),
      size: 'xl',
    }"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-ink-gray-9 mb-2">
            {{ __('Lead') }}
          </label>
          <div class="text-base text-ink-gray-7">
            {{ leadName }}
          </div>
        </div>
        
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
          v-model="reminder.type"
          :label="__('Reminder Type')"
          type="select"
          :options="reminderTypes"
          :placeholder="__('Select type')"
        />
        
        <FormControl
          v-model="reminder.remarks"
          :label="__('Remarks')"
          type="textarea"
          :placeholder="__('Add remarks...')"
          :rows="4"
        />
      </div>
    </template>
    
    <template #actions>
      <Button
        variant="solid"
        :label="__('Save Reminder')"
        :loading="savingReminder"
        @click="saveReminder"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, FormControl, Button, call, createResource } from 'frappe-ui'

const props = defineProps({
  leadId: {
    type: String,
    required: true,
  },
  leadName: {
    type: String,
    required: true,
  },
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue'])

const show = ref(props.modelValue)
const savingReminder = ref(false)

const reminderTypes = [
  { label: __('Follow Up Call'), value: 'Follow Up Call' },
  { label: __('Demo'), value: 'Demo' },
  { label: __('Meeting'), value: 'Meeting' },
  { label: __('Email'), value: 'Email' },
  { label: __('Other'), value: 'Other' },
]

const reminder = ref({
  date: '',
  time: '',
  type: '',
  remarks: '',
})

watch(
  () => props.modelValue,
  (val) => {
    show.value = val
    if (val) {
      // Reset form when modal opens
      reminder.value = {
        date: '',
        time: '',
        type: '',
        remarks: '',
      }
    }
  }
)

watch(show, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    reminder.value = {
      date: '',
      time: '',
      type: '',
      remarks: '',
    }
  }
})

async function saveReminder() {
  if (!reminder.value.date || !reminder.value.time || !reminder.value.type) {
    window.frappe?.show_alert({
      message: __('Please fill all required fields'),
      indicator: 'red',
    })
    return
  }
  
  savingReminder.value = true
  
  try {
    // Combine date and time
    const dueDate = `${reminder.value.date} ${reminder.value.time}`
    
    // Create a CRM Task as reminder
    await call('frappe.client.insert', {
      doc: {
        doctype: 'CRM Task',
        title: `${reminder.value.type} - ${props.leadName}`,
        reference_doctype: 'CRM Lead',
        reference_docname: props.leadId,
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
    
    // Reload the page to update counts
    if (window.location) {
      window.location.reload()
    }
  } catch (error) {
    console.error('Error creating reminder:', error)
    window.frappe?.show_alert({
      message: __('Failed to create reminder'),
      indicator: 'red',
    })
  } finally {
    savingReminder.value = false
  }
}
</script>

