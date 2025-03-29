import React from "react";
import { BsFillVolumeUpFill, BsFillVolumeMuteFill } from 'react-icons/bs';

interface VolumeControlProps {
    onVolumeChange: (newVolume: number) => void;
    volume: number;
}

const VolumeControl: React.FC<VolumeControlProps> = ({ onVolumeChange, volume }) => {
    const handleVolumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newVolume = parseFloat(event.target.value);
        onVolumeChange(newVolume);
    };

    return (
        <div className="mt-4 flex items-center justify-center">
            {volume > 0.1 ? (
                BsFillVolumeUpFill({ size: 24, className: "text-white mr-2" })
            ) : (
                BsFillVolumeMuteFill({ size: 24, className: "text-white mr-2" })
            )}
            <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={volume}
                onChange={handleVolumeChange}
            />
        </div>
    );
};

export default VolumeControl;

