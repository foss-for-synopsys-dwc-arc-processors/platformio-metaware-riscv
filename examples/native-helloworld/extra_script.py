Import("env")

# In-line command with arguments
env.Replace(
    UPLOADCMD="nsimdrv -prop=nsim_isa_family=rv32 -prop=nsim_isa_ext=-all.i.zicsr.zifencei.zihintpause.b.zca.zcb.zcmp.zcmt.a.m.zbb -prop=nsim_semihosting=1 -off=enable_exceptions  $SOURCE"
)