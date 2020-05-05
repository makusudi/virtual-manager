<template>
  <div class="container-fluid pb-5">
    <a-page-header title="Virtual Machines">
      <template slot="extra">
        <VMCreateModal @addNewVM="handleNewVM" />
      </template>
      <a-row type="flex">
        <a-statistic title="Hardware Status" :value="apiResponse === false ? 'Pending' : 'Running'" class="mr-5" />
        <a-statistic title="Total Quantity" suffix="VMs" :value="countTotalVMs" class="mr-5" />
        <a-statistic title="CPU Total" suffix="cores" :value="countTotalCPU" class="mr-5" />
        <a-statistic title="RAM Total" suffix="GB" :value="countTotalRAM" class="mr-5" />
        <a-statistic title="HDD Total" suffix="GB" :value="countTotalHDD" />
      </a-row>
    </a-page-header>
    <div v-if="apiResponse" class="row mt-4 px-4 animated fadeIn">
      <div
        v-for="(vm, index) in vmArray"
        :key="'vm' + index"
        class="col-xl-2 col-lg-3 col-md-6 col-sm-12 mb-4">
        <VM :vm-obj="vm" @VMDelete="VMDelete" />
      </div>
    </div>
    <div v-else class="d-flex justify-content-center align-items-center" style="height: 50vh">
      <a-spin tip="Emulating work for 2 seconds..." size="large" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import VM from '@/components/VirtualMachine/VM'
import VMCreateModal from '@/components/VirtualMachine/VMCreateModal'

export default {
  components: {
    VM,
    VMCreateModal
  },
  data () {
    return {
      vmArray: [],
      apiResponse: false,
      totalCPU: 0,
      totalRAM: 0,
      totalHDD: 0,
      totalVMs: 0
    }
  },
  computed: {
    countTotalVMs () {
      return this.vmArray.length
    },
    countTotalCPU () {
      let totalCPU = 0
      for (const vm of this.vmArray) {
        totalCPU = totalCPU + vm.cpu
      }
      return totalCPU
    },
    countTotalHDD () {
      let totalHDD = 0
      for (const vm of this.vmArray) {
        totalHDD = totalHDD + vm.hdd
      }
      return totalHDD
    },
    countTotalRAM () {
      let totalRAM = 0
      for (const vm of this.vmArray) {
        totalRAM = totalRAM + vm.ram
      }
      return totalRAM
    }
  },
  beforeMount () {
    axios({
      method: 'GET',
      headers: { Authorization: 'token', 'Content-Type': 'application/json' },
      url: `http://${window.location.hostname}:8080/api/my_vms?owner=admin`
    }).then((response) => {
      this.vmArray = response.data.result
      setTimeout(() => {
        this.apiResponse = true
      }, 2000)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    VMDelete (vmObject) {
      this.vmArray.splice(this.vmArray.indexOf(vmObject), 1)
    },
    handleNewVM (object) {
      this.vmArray.push(object)
    }
  }
}
</script>

<style>

</style>
