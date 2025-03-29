import React from 'react';

interface ProgressBarProps {
  currentTime: number;
  duration: number;
  onSeek: (newTime: number) => void;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ currentTime, duration, onSeek }) => {
  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;
  const progressBarRef = React.useRef<HTMLDivElement>(null)
  const handleClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if(progressBarRef.current){
        const rect = progressBarRef.current.getBoundingClientRect()
        const offset = event.clientX - rect.left;
        const totalWidth = rect.width;
        const newTime = (offset / totalWidth) * duration;
        onSeek(newTime)
    }
  }
  return (
    <div className="mt-4">
      <div className="bg-gray-700 h-2 rounded-full relative" onClick={handleClick} ref={progressBarRef}>
        <div className="bg-green-500 h-2 rounded-full absolute" style={{ width: `${progress}%` }}></div>
      </div>
    </div>
  );
};

export default ProgressBar;
