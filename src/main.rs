#![feature(alloc_error_handler)]
#![feature(maybe_uninit_uninit_array)]
#![feature(maybe_uninit_slice)]
#![feature(maybe_uninit_array_assume_init)]
#![no_builtins]
#![no_std]
#![no_main]
extern crate alloc;

use core::arch::asm;
mod allocator;
#[allow(dead_code)]
mod io;
mod solution;
#[allow(dead_code)]
mod sorts;

#[global_allocator]
static ALLOC: allocator::Allocator = allocator::Allocator;

#[no_mangle]
#[link_section = ".init"]
fn _start() {
    unsafe {
        asm!("and rsp, 0xFFFFFFFFFFFFFFF0");
    }
    solution::main();
    unsafe {
        asm!("syscall", in("rax") 231, in("rdi") 0);
    }
}

#[cfg(not(test))]
#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}

#[cfg(not(test))]
#[alloc_error_handler]
fn alloc_fail(_: core::alloc::Layout) -> ! {
    unsafe { core::hint::unreachable_unchecked() }
}

#[cfg(feature = "no-probe")]
#[no_mangle]
fn __rust_probestack() {}
