<template>
  <a-card hoverable size="small" :title="vmObj.name">
    <template slot="actions" class="ant-card-actions" style="height: 20px !important;">
      <VMConfigModal :vm="vmObj"/>
      <VMDescriptionModal :vm="vmObj"/>
      <a-popconfirm
        :title="`Delete ${vmObj.name}?`"
        ok-text="Yes"
        cancel-text="No"
        placement="bottom"
        @confirm="confirmDeleting"
        @cancel="cancelDeleting">
        <a-icon slot="icon" type="question-circle-o" style="color: red"/>
        <a href="#">
          <a-icon key="delete" type="delete"/>
        </a>
      </a-popconfirm>
    </template>
    <p class="p-0 m-0 pt-2 d-flex align-items-center">
      <mdb-icon icon="microchip"/>
      <span class="ml-1 font-weight-normal">
          CPU: {{ vmObj.cpu }}
      </span>
    </p>
    <p class="p-0 m-0 d-flex align-items-center">
      <mdb-icon icon="memory"/>
      <span class="ml-1 font-weight-normal">
          RAM: {{ vmObj.ram }} GB
        </span>
    </p>
    <p class="p-0 m-0 d-flex align-items-center">
      <mdb-icon icon="hdd"/>
      <span class="ml-1 font-weight-normal">
          HDD: {{ vmObj.hdd }} GB
        </span>
    </p>
    <p class="p-0 m-0 d-flex align-items-center">
        <span class="font-weight-normal">
          Description: {{ vmObj.description }}
        </span>
    </p>
  </a-card>
</template>

<script>
import { mdbIcon } from 'mdbvue'
import axios from 'axios'
import VMConfigModal from './VMConfigModal'
import VMDescriptionModal from './VMDescriptionModal'

export default {
  name: 'VM',
  components: {
    VMConfigModal,
    VMDescriptionModal,
    mdbIcon
  },
  props: {
    vmObj: Object
  },
  data () {
    return {
      current: ['index']
    }
  },
  methods: {
    confirmDeleting () {
      this.$message.warning(`Trying to delete ${this.vmObj.name}...`)
      axios({
        method: 'POST',
        headers: {
          Authorization: 'token',
          'Content-Type': 'application/json'
        },
        url: 'http://127.0.0.1:8080/api/delete_vm',
        data: { name: this.vmObj.name }
      }).then((response) => {
        this.$message.success(`Virtual machine ${this.vmObj.name} has been successfully deleted from your scope`)
        this.$emit('VMDelete', this.vmObj)
      }).catch((error) => {
        this.$message.success(`An error occured in ${this.vmObj.name} deleting process :(`)
        console.log(error)
      })
    },
    cancelDeleting () {

    }
  }
}
</script>

<style>
  .ant-card-body {
    padding-top: 0.7rem !important;
  }

  ul.ant-card-actions {
    display: flex;
    align-items: flex-start;
  }

  ul.ant-card-actions li {
    margin-top: 0.1rem;
    margin-bottom: 0.3rem;
  }

  a#card_link {
    color: #47494e !important;
  }

  i.anticon.anticon-setting {
    width: 100%;
    height: 100%;
  }

  i.anticon.anticon-edit {
    width: 100%;
    height: 100%;
  }

  i.anticon.anticon-delete {
    width: 100%;
    height: 100%;
  }
</style>
