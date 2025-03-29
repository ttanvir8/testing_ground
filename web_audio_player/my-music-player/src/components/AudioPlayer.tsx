import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';
import ProgressBar from './ProgressBar';
import Controls from './Controls';
import TrackInfo from './TrackInfo';
import VolumeControl from './VolumeControl';
import {BsPlayFill, BsPauseFill, BsFillSkipStartFill, BsFillSkipEndFill} from 'react-icons/bs'

const AudioPlayer: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [duration, setDuration] = useState<number>(0);
  const [volume, setVolume] = useState<number>(1);
  const audioRef = useRef<HTMLAudioElement>(null);

  const trackName = "Sample Song"; // Replace with actual track info if needed
  const artist = "Unknown Artist";    // Replace with actual artist info if needed

  const togglePlayPause = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleSeek = (newTime: number) => {
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    const key = event.key;
    if (key >= '0' && key <= '9') {
      const percentage = parseInt(key) * 10;
      const newTime = (percentage / 100) * duration;
      handleSeek(newTime);
    }
  };

  const handleVolumeChange = (newVolume: number) => {
    if (audioRef.current) {
        audioRef.current.volume = newVolume;
        setVolume(newVolume)
    }
  }

  const skipBackward = () => {
    if (audioRef.current) {
      audioRef.current.currentTime -= 10; // Skip back 10 seconds
    }
  };
  const skipForward = () => {
    if (audioRef.current) {
      audioRef.current.currentTime += 10; // Skip forward 10 seconds
    }
  };

  useEffect(() => {
    if(audioRef.current){
        audioRef.current.volume = volume;
    }
  },[volume])

  useEffect(() => {
    if (audioRef.current) {
        const audio = audioRef.current;
        audio.addEventListener('timeupdate', handleTimeUpdate);
        audio.addEventListener('loadedmetadata', handleLoadedMetadata);
        return () => {
            audio.removeEventListener('timeupdate', handleTimeUpdate);
            audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
        };
    }
    }, []);

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg w-96" onKeyDown={handleKeyDown} tabIndex={0}>
      <TrackInfo trackName={trackName} artist={artist} />
      <ProgressBar currentTime={currentTime} duration={duration} onSeek={handleSeek} />
      <Controls isPlaying={isPlaying} onPlayPause={togglePlayPause} skipBackward={skipBackward} skipForward={skipForward}/>
      <VolumeControl onVolumeChange={handleVolumeChange} volume={volume} />
      <audio ref={audioRef} src="/audio/sample.mp3"></audio> {/* Change this to your mp3 file */}
    </div>
  );
};

export default AudioPlayer;
