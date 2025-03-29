import React from 'react';
import { BsPlayFill, BsPauseFill, BsFillSkipStartFill, BsFillSkipEndFill } from 'react-icons/bs';

interface ControlsProps {
  isPlaying: boolean;
  onPlayPause: () => void;
  skipBackward: () => void;
  skipForward: () => void;
}

const Controls: React.FC<ControlsProps> = ({ isPlaying, onPlayPause, skipBackward, skipForward }) => {
  return (
    <div className="mt-4 flex justify-center space-x-4 items-center">
      <button className='text-white' onClick={skipBackward}>
        {BsFillSkipStartFill({ size: 32 })}
      </button>
      <button className="bg-green-500 text-white p-2 rounded-full" onClick={onPlayPause}>
        {isPlaying ? BsPauseFill({ size: 32 }) : BsPlayFill({ size: 32 })}
      </button>
      <button className='text-white' onClick={skipForward}>
        {BsFillSkipEndFill({ size: 32 })}
      </button>
    </div>
  );
};

export default Controls;
