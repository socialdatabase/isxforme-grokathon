export default defineAppConfig({
ui: {
    // card: {
    //   slots: {
    //     header: 'p-4 sm:p-5',
    //     body: 'p-4 sm:p-5',
    //     footer: 'p-4 sm:p-5',
    //   },
    //   variants: {
    //     variant: {
    //       solid: {
    //         root: 'text-card rounded-xl bg-card ring-card ring-1',
    //       },
    //       subtle: {
    //         root: 'bg-elevated ring-1 ring-elevated',
    //       },
    //     },
    //   },
    // },
    // input: {
    //   slots: {
    //     base: 'rounded-full w-full h-14',
    //   },
    //   compoundVariants: [
    //     {
    //       color: 'primary',
    //       variant: 'outline',
    //       class: 'text-md bg-card ring-card text-default focus-visible:ring-accented',
    //     },
    //   ],

    // },
    tabs:{
      variants: {
        variant: {
          pill: {
            list: 'rounded-full bg-card',
            indicator: 'rounded-full',
          },
        },
        size: {
          xl: {
            trigger: 'md:px-3 md:py-2 md:text-base md:gap-2 px-2.5 py-1.5 text-xs gap-1.5',
          }
        },
      },
      compoundVariants: [
        {
          color: 'primary',
          variant: 'pill',
          class: {
            list: 'p-[3px] md:h-16 h-10',
            indicator: 'bg-white',
            trigger: 'data-[state=active]:text-black! text-dimmed!',
          },
        },
      ],
    },
},
})