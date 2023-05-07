use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use device_query::{DeviceQuery, DeviceState, Keycode};
use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

// 假设 speech2text 函数如下
fn speech2text(_audio_buffer: &[i16]) -> String {
    String::new()
}

fn main() {
    let device_state = DeviceState::new();
    let host = cpal::default_host();
    let input_device = host.default_input_device().expect("没有找到输入设备");
    let config = input_device
        .default_input_config()
        .expect("没有找到默认输入配置");
    println!("默认输入设备: {:?}", input_device.name());
    println!("默认输入配置: {:?}", config);

    let config: cpal::StreamConfig = config.config();
    let sample_rate = config.sample_rate.0 as usize;
    let channels = config.channels as usize;
    let buffer_duration = 1000; // 1秒
    let buffer_len = buffer_duration * sample_rate * channels / 1000;

    let audio_buffer: Arc<Mutex<VecDeque<i16>>> = Arc::new(Mutex::new(VecDeque::new()));

    let data_callback = move |data: &[i16], _: &cpal::InputCallbackInfo| {
        let mut audio_buffer = audio_buffer.lock().unwrap();
        for &sample in data {
            audio_buffer.push_back(sample);
            if audio_buffer.len() > buffer_len {
                audio_buffer.pop_front();
            }
        }
    };

    let error_callback = |err| eprintln!("输入流错误: {:?}", err);

    let stream = input_device
        .build_input_stream(&config, data_callback, error_callback, None)
        .unwrap();
    stream.play().unwrap();

    loop {
        let keys = device_state.get_keys();
        if keys.contains(&Keycode::I) {
            println!("按下了I键，开始录音...");
            let audio_buffer_copy = {
                let audio_buffer = audio_buffer.lock().unwrap();
                audio_buffer.clone()
            };
            let text = speech2text(&audio_buffer_copy.make_contiguous());
            println!("录音转换为文字: {}", text);
        }
    }
}
